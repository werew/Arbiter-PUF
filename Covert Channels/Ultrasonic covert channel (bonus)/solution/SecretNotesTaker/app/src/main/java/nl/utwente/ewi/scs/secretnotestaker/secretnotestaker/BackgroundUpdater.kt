package nl.utwente.ewi.scs.secretnotestaker.secretnotestaker

import android.graphics.BitmapFactory
import android.preference.PreferenceManager
import android.util.Log
import java.net.HttpURLConnection
import java.net.URL
import android.media.AudioTrack

class BackgroundUpdater(var activity: TakesNotesActivity?) : Runnable {
    private var stopNow = false
    private lateinit var thread: Thread
    private var track : AudioTrack? = null

    fun start() {
        thread = Thread(this)
        stopNow = false
        thread.start()
    }

    fun stop() {
        activity = null
        stopNow = true
        thread.interrupt()
    }

    fun getUrl(): String {
        val sharedPref = PreferenceManager.getDefaultSharedPreferences(activity)
        val url = sharedPref.getString("url", "")
        // url should contain the URL to the cat image server without the trailing /randomcat

        if (url.takeLast(1) == "/") {
            return url + "randomcat"
        } else {
            return url + "/randomcat"
        }
    }

    override fun run() {
        while (true) {
            if (stopNow) {
                // Activity has been terminated, also terminate the thread
                return
            }
            try {
                // Get the URL of our randomcat server
                val url = URL(getUrl())

                // Open an HTTP connection to that URL
                val urlConnection = url.openConnection() as HttpURLConnection

                try {
                    // Try to decode a bitmap from the server response
                    var bitmap = BitmapFactory.decodeStream(urlConnection.inputStream)

                    // Update the activity with the new images.
                    activity!!.runOnUiThread(UpdateImageRequest(bitmap, activity!!))
                } catch (e: Exception) {
                    Log.e("Network", "HTTP request failed for URL: " + url + " or download problem", e)
                } finally {
                    urlConnection.disconnect()
                }
            } catch (e: Exception) {
                Log.e("Network", "Problem with download", e)
            }
            Log.d("Background", "Completed network operation, now sleeping")
            try {
                Thread.sleep(5000)
            } catch (e: InterruptedException) {

            }
        }
    }
}