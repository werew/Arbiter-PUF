package nl.utwente.ewi.scs.secretnotestaker.secretnotestaker

import android.media.AudioTrack
import android.media.AudioManager
import android.media.AudioFormat

import android.util.Log

import java.util.BitSet
import java.util.Base64

class AudioEncoder() {
    private fun encodeMessage(s : String) : List<Boolean> {
        val digits = s.map { it.toString().toInt() }
        val bits = mutableListOf<Boolean>()

        bits.add(false)

        for (digit in digits) {
            for (i in 0 until digit + 1) {
                bits.add(true)
                bits.add(false)
            }

            bits.add(false)
            bits.add(false)
        }

        bits.add(false)
        bits.add(false)

        return bits
    }

    fun encode(data : String, frequency : Int = 20000, blockDuration : Int = 200, fadeDuration : Int = 20) : AudioTrack {
        val bits = encodeMessage(data)

        val sampleRate = 44100
        val samplesPerBit : Int = (sampleRate * blockDuration) / 1000

        val samples = ShortArray(bits.size * samplesPerBit)

        // create a linear envelope to prevent clicking noises
        val envelope = FloatArray(samplesPerBit)
        val samplesPerFade : Int = (sampleRate * fadeDuration) / 1000

        for (i in 0 until samplesPerBit) {
            if ( i < samplesPerFade) {
                envelope[i] = i.toFloat() / samplesPerFade.toFloat()
            } else if (i > samplesPerBit - samplesPerFade) {
                envelope[i] = (samplesPerBit - i).toFloat() / samplesPerFade.toFloat()
            } else {
                envelope[i] = 1.toFloat()
            }
        }

        for (i in 0 until bits.size) {
            var angle = 0.0
            val increment = (2 * Math.PI * frequency / sampleRate)

            for (j in 0 until samplesPerBit) {
                val bit = bits.get(i)

                if (bit) {
                    val sample = Math.sin((2 * Math.PI * frequency / sampleRate) * j) * envelope[j]

                    samples.set(i * samplesPerBit + j, (sample * Short.MAX_VALUE).toShort())
                    angle += increment
                } else {
                    samples.set(i * samplesPerBit + j, 0)
                }
            }
        }

        val track = AudioTrack(AudioManager.STREAM_MUSIC,
            sampleRate, AudioFormat.CHANNEL_CONFIGURATION_MONO,
            AudioFormat.ENCODING_PCM_16BIT, samples.size * 2,
            AudioTrack.MODE_STATIC)

        track.write(samples, 0, samples.size)

        return track
    }
}
