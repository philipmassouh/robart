const { app, BrowserWindow } = require('electron')
const path = require('path')

function createWindow () {
    const win = new BrowserWindow({
        width: 1800,
        height: 900,
        frame: false,
        roundedCorners: true,
        title: "ROBART",
        icon: path.join(__dirname, "assets/robartIcon.png"),
        webPreferences: {
            preload: path.join(__dirname, "scripts/preload.js"),
            contextIsolation: true,
            enableRemoteModule: true
        }
    })

    //win.menuBarVisible = false
    win.loadFile('index.html')
}

app.whenReady().then(() => {
    createWindow()

    /* Opens a window on current app on mac. */
    app.on('activate', function () {
        if (BrowserWindow.getAllWindows().length === 0) createWindow()
    })
})


/* Closes process when all windows are closed on windows and linux. */
app.on('window-all-closed', function () {
    if (process.platform !== 'darwin') app.quit()
})

