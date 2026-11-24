class HabitRepository(private val habitDao: HabitDao) {
    suspend fun createHabit(title: String, targetPerDay: Int, startDateEpoch: Long): Long {
        val habit = HabitEntity(
            title = title,
            targetFrequency = targetPerDay,
            startDate = startDateEpoch
        )
        return habitDao.insertHabit(habit)
    }

    fun getAllHabits() = habitDao.observeAllHabits()
}
