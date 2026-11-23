package org.telegram.messenger;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.net.Uri;
import android.widget.Toast;

import org.json.JSONArray;
import org.json.JSONObject;
import org.telegram.ui.ActionBar.BaseFragment;

import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.io.OutputStream;
import java.nio.charset.StandardCharsets;
import java.util.HashSet;
import java.util.Iterator;
import java.util.Map;
import java.util.Set;

/*
 * AmberGram fork (round 19 — extras): settings backup.
 * Source inspiration: Nnngram #63 (fork settings backup).
 * Every AmberGram flag lives in MessagesController.getGlobalMainSettings() under
 * an "amber" prefix (AmberGhost, AmberAntiAds, AmberMorphe, AmberChatTweaks,
 * AmberPrivacy, AmberExtras, AmbergramProxyManager toggle, ...), so backup =
 * dump all "amber*" prefs to a JSON document the user picks with the system
 * file picker, and restore = apply the JSON back by value type. Unknown (newer)
 * amber keys are applied blindly, so backups stay forward-compatible.
 * JSON is built with org.json, which is bundled with Android — no extra dependency.
 *
 * Wiring: call exportSettings(parent)/importSettings(parent) from the hub rows,
 * and in the hub fragment override onActivityResultFragment(...) to forward:
 *     if (AmberBackup.handleActivityResult(requestCode, resultCode, data)) return;
 * Restart the app after an import — the flag classes cache their booleans.
 */
public class AmberBackup {

    public static final int REQUEST_EXPORT_SETTINGS = 97531;
    public static final int REQUEST_IMPORT_SETTINGS = 97532;

    private static final String PREFS_PREFIX = "amber";
    private static final String SUGGESTED_FILE_NAME = "ambergram-settings.json";

    // ---------------------------------------------------------------- export

    public static void exportSettings(BaseFragment parent) {
        try {
            Intent intent = new Intent(Intent.ACTION_CREATE_DOCUMENT);
            intent.addCategory(Intent.CATEGORY_OPENABLE);
            intent.setType("application/json");
            intent.putExtra(Intent.EXTRA_TITLE, SUGGESTED_FILE_NAME);
            if (parent != null) {
                parent.startActivityForResult(intent, REQUEST_EXPORT_SETTINGS);
            }
        } catch (Throwable t) {
            FileLog.e(t);
            toast(parent, LocaleController.getString(R.string.AmberBackupFailed));
        }
    }

    // ---------------------------------------------------------------- import

    public static void importSettings(BaseFragment parent) {
        try {
            Intent intent = new Intent(Intent.ACTION_OPEN_DOCUMENT);
            intent.addCategory(Intent.CATEGORY_OPENABLE);
            intent.setType("application/json");
            if (parent != null) {
                parent.startActivityForResult(intent, REQUEST_IMPORT_SETTINGS);
            }
        } catch (Throwable t) {
            FileLog.e(t);
            toast(parent, LocaleController.getString(R.string.AmberBackupFailed));
        }
    }

    // ---------------------------------------------------------------- results

    /**
     * Forward from the parent fragment's onActivityResultFragment.
     * Returns true when the (requestCode, resultCode, data) triple belongs to us
     * and has been consumed (even when the user simply cancelled the picker).
     */
    public static boolean handleActivityResult(int requestCode, int resultCode, Intent data) {
        if (requestCode != REQUEST_EXPORT_SETTINGS && requestCode != REQUEST_IMPORT_SETTINGS) {
            return false;
        }
        try {
            if (resultCode != Activity.RESULT_OK || data == null || data.getData() == null) {
                return true; // picker cancelled — nothing to do
            }
            Uri uri = data.getData();
            if (requestCode == REQUEST_EXPORT_SETTINGS) {
                exportToFile(uri);
            } else {
                importFromUri(uri);
            }
        } catch (Throwable t) {
            FileLog.e(t);
            toast(null, LocaleController.getString(R.string.AmberBackupFailed));
        }
        return true;
    }

    // ---------------------------------------------------------------- internals

    private static void exportToFile(Uri uri) throws Exception {
        JSONObject object = collectSettings();
        OutputStream stream = ApplicationLoader.applicationContext.getContentResolver().openOutputStream(uri);
        if (stream == null) {
            throw new IllegalStateException("openOutputStream returned null");
        }
        try {
            stream.write(object.toString().getBytes(StandardCharsets.UTF_8));
            stream.flush();
        } finally {
            try {
                stream.close();
            } catch (Exception ignore) {
            }
        }
        FileLog.d("AmberBackup: exported " + object.length() + " amber settings");
    }

    private static void importFromUri(Uri uri) throws Exception {
        InputStream input = ApplicationLoader.applicationContext.getContentResolver().openInputStream(uri);
        if (input == null) {
            throw new IllegalStateException("openInputStream returned null");
        }
        byte[] buffer;
        try {
            ByteArrayOutputStream output = new ByteArrayOutputStream();
            byte[] chunk = new byte[8192];
            int read;
            while ((read = input.read(chunk)) > 0) {
                output.write(chunk, 0, read);
            }
            buffer = output.toByteArray();
        } finally {
            try {
                input.close();
            } catch (Exception ignore) {
            }
        }
        JSONObject object = new JSONObject(new String(buffer, StandardCharsets.UTF_8));
        applySettings(object);
        toast(null, LocaleController.getString(R.string.AmberBackupDone));
    }

    private static JSONObject collectSettings() throws Exception {
        SharedPreferences preferences = MessagesController.getGlobalMainSettings();
        Map<String, ?> all = preferences.getAll();
        JSONObject object = new JSONObject();
        if (all == null) {
            return object;
        }
        for (Map.Entry<String, ?> entry : all.entrySet()) {
            String key = entry.getKey();
            Object value = entry.getValue();
            if (key == null || !key.startsWith(PREFS_PREFIX) || value == null) {
                continue;
            }
            try {
                if (value instanceof Boolean) {
                    object.put(key, (Boolean) value);
                } else if (value instanceof Integer) {
                    object.put(key, (Integer) value);
                } else if (value instanceof Long) {
                    object.put(key, (Long) value);
                } else if (value instanceof Float) {
                    object.put(key, (Float) value);
                } else if (value instanceof String) {
                    object.put(key, (String) value);
                } else if (value instanceof Set) {
                    JSONArray array = new JSONArray();
                    for (Object item : (Set<?>) value) {
                        if (item != null) {
                            array.put(String.valueOf(item));
                        }
                    }
                    object.put(key, array);
                }
            } catch (Exception e) {
                FileLog.e(e);
            }
        }
        return object;
    }

    private static void applySettings(JSONObject object) {
        SharedPreferences.Editor editor = MessagesController.getGlobalMainSettings().edit();
        Iterator<String> keys = object.keys();
        while (keys.hasNext()) {
            String key = keys.next();
            if (key == null || !key.startsWith(PREFS_PREFIX)) {
                continue; // never touch non-Amber settings, even in a hand-edited file
            }
            try {
                Object value = object.get(key);
                if (value instanceof Boolean) {
                    editor.putBoolean(key, (Boolean) value);
                } else if (value instanceof Integer) {
                    editor.putInt(key, (Integer) value);
                } else if (value instanceof Long) {
                    editor.putLong(key, (Long) value);
                } else if (value instanceof Double) {
                    editor.putFloat(key, (float) (double) (Double) value);
                } else if (value instanceof String) {
                    editor.putString(key, (String) value);
                } else if (value instanceof JSONArray) {
                    JSONArray array = (JSONArray) value;
                    Set<String> set = new HashSet<>();
                    for (int a = 0; a < array.length(); a++) {
                        String item = array.optString(a, null);
                        if (item != null) {
                            set.add(item);
                        }
                    }
                    editor.putStringSet(key, set);
                }
            } catch (Exception e) {
                // one bad key must never kill the whole import
                FileLog.e(e);
            }
        }
        editor.apply();
    }

    private static void toast(BaseFragment parent, String message) {
        AndroidUtilities.runOnUIThread(() -> {
            try {
                Context context = parent != null && parent.getParentActivity() != null
                        ? parent.getParentActivity()
                        : ApplicationLoader.applicationContext;
                Toast.makeText(context, message, Toast.LENGTH_SHORT).show();
            } catch (Throwable ignore) {
            }
        });
    }
}
