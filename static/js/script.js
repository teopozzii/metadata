// Metadata App - JavaScript utilities

function openFolderPicker(callback) {
    window.pywebview.api.select_folder().then(function(folderPath) {
        if (folderPath) {
            callback(folderPath);
        }
    });
}
