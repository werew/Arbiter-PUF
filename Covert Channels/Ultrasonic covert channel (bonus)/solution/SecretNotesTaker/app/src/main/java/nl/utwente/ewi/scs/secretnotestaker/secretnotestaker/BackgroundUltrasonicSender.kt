package nl.utwente.ewi.scs.secretnotestaker.secretnotestaker

import android.preference.PreferenceManager
import android.util.Log
import android.media.AudioTrack

class BackgroundUltrasonicSender(var activity: TakesNotesActivity?) : Runnable {
    private var stopNow = false
    private lateinit var thread: Thread

    private var pin: String? = null
    private var pinChanged = false

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

    fun setPin(pin : String) {
        this.pin = pin
        this.pinChanged = true
    }

    override fun run() {
        var encoder = AudioEncoder()
        val sharedPref = PreferenceManager.getDefaultSharedPreferences(activity)
        var track : AudioTrack? = null

        while (true) {
            if (stopNow) {
                if (track != null && track.getPlayState() != AudioTrack.STATE_UNINITIALIZED) {
                    track.pause()
                    track.release()
                }

                break
            }

            if (pinChanged && pin != null) {
                pinChanged = false

                if (track != null && track.getPlayState() != AudioTrack.STATE_UNINITIALIZED) {
                    track.pause()
                    track.release()
                }

                val frequency = sharedPref.getString("frequency", "").toIntOrNull() ?: 20000
                val blockDuration = sharedPref.getString("block_duration", "").toIntOrNull() ?: 200
                val fadeDuration = sharedPref.getString("fade_duration", "").toIntOrNull() ?: 20

                track = encoder.encode(pin!!, frequency, blockDuration, fadeDuration)
                track.setLoopPoints(0, track.getBufferSizeInFrames(), -1)
                track.play()
            }

            try {
                Thread.sleep(1000)
            } catch (e: InterruptedException) {

            }
        }
    }
}
