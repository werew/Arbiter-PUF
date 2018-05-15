package nl.utwente.ewi.scs.secretnotestaker.secretnotestaker

import android.app.Activity
import android.os.Bundle


class SettingsActivity : Activity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        fragmentManager.beginTransaction()
                .replace(android.R.id.content, SettingsFragment())
                .commit()
    }
}