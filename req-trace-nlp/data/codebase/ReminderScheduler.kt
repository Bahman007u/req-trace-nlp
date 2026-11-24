class ReminderScheduler(private val context: Context) {
    fun scheduleDailyReminder(habitId: Long, hourOfDay: Int, minute: Int) {
        // Configures alarm and posts local reminder notification at chosen time
        val notificationTitle = "Daily Habit Reminder"
        AlarmManagerHelper.setRepeatingAlarm(context, habitId, hourOfDay, minute, notificationTitle)
    }
}
