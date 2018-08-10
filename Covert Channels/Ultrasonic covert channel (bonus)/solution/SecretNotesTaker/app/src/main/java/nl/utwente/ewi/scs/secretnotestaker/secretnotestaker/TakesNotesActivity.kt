package nl.utwente.ewi.scs.secretnotestaker.secretnotestaker

import android.content.Intent
import android.graphics.Bitmap
import android.os.Bundle
import android.support.v7.app.AppCompatActivity
import android.view.Menu
import android.view.MenuItem
import android.widget.ImageView
import android.widget.EditText
import kotlinx.android.synthetic.main.activity_takes_notes.*
import android.text.TextWatcher
import android.text.Editable

import android.util.Log

class PinWatcher(var activity : TakesNotesActivity?) : TextWatcher {
    override fun beforeTextChanged(p0: CharSequence, p1: Int, p2: Int, p3: Int) : Unit { }
    override fun onTextChanged(p0: CharSequence, p1: Int, p2: Int, p3: Int) : Unit { }

    override fun afterTextChanged(p0: Editable) : Unit {
        val pin = p0.toString()
        val pinRegex = """[0-9]{4}""".toRegex()

        if (pinRegex.matchEntire(pin) != null) {
            activity!!.ultrasonicSender.setPin(pin)
        }
    }
}

class TakesNotesActivity : AppCompatActivity() {
    lateinit var updater: BackgroundUpdater
    lateinit var ultrasonicSender: BackgroundUltrasonicSender

    fun updateImage(bitmap: Bitmap) {
        val view = findViewById<ImageView>(R.id.imageView)
        view.setImageBitmap(bitmap)
    }

    override fun onResume() {
        super.onResume()
        updater = BackgroundUpdater(this)
        updater.start()

        ultrasonicSender = BackgroundUltrasonicSender(this)
        ultrasonicSender.start()

        val view = findViewById<EditText>(R.id.editText)
        view.addTextChangedListener(PinWatcher(this))

        val pin = (view.getText() ?: "").toString()
        val pinRegex = """[0-9]{4}""".toRegex()

        if (pinRegex.matchEntire(pin) != null) {
            ultrasonicSender.setPin(pin)
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_takes_notes)
        setSupportActionBar(toolbar)

        val view = findViewById<EditText>(R.id.editText)
        view.addTextChangedListener(PinWatcher(this))
    }

    override fun onPause() {
        super.onPause()
        updater.stop()
        ultrasonicSender.stop()
    }

    override fun onCreateOptionsMenu(menu: Menu): Boolean {
        menuInflater.inflate(R.menu.menu_takes_notes, menu)
        return true
    }

    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        return when (item.itemId) {
            R.id.action_settings -> {
                val intent = Intent(this, SettingsActivity::class.java)
                startActivity(intent)
                return true

            }
            else -> super.onOptionsItemSelected(item)
        }
    }
}
