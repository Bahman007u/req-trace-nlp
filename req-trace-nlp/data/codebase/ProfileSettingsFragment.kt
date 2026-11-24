class ProfileSettingsFragment {
    fun filterItems(query: String, items: List<String>): List<String> {
        return items.filter { it.contains(query, ignoreCase = true) }
    }

    fun updateUserProfile(displayName: String, preferencesEnabled: Boolean) {
        SessionPrefs.saveProfile(name = displayName, enabled = preferencesEnabled)
    }
}
