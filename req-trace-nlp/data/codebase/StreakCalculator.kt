class StreakCalculator {
    fun markCompletedToday(logs: List<CompletionLog>, todayEpochDay: Long): Int {
        val updatedLogs = logs + CompletionLog(day = todayEpochDay, completed = true)
        return computeCurrentStreak(updatedLogs)
    }

    private fun computeCurrentStreak(logs: List<CompletionLog>): Int {
        return logs.count { it.completed }
    }
}
