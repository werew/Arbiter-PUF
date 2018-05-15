package nl.utwente.ewi.scs.secretnotestaker.secretnotestaker

import android.content.Intent
import android.graphics.Bitmap
import android.os.Bundle
import android.support.v7.app.AppCompatActivity
import android.view.Menu
import android.view.MenuItem
import android.widget.ImageView
import kotlinx.android.synthetic.main.activity_takes_notes.*


class TakesNotesActivity : AppCompatActivity() {
    lateinit var updater: BackgroundUpdater

    fun updateImage(bitmap: Bitmap) {
        val view = findViewById<ImageView>(R.id.imageView)
        view.setImageBitmap(bitmap)
    }

    override fun onResume() {
        super.onResume()
        updater = BackgroundUpdater(this)
        updater.start()
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_takes_notes)
        setSupportActionBar(toolbar)
    }

    override fun onPause() {
        super.onPause()
        updater.stop()
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
