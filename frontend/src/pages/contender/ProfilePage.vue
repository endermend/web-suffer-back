<template>
  <main>
    <div class="main_contents page_enter">
      <ProfileHero :key="$route.fullPath" />

      <!-- stats -->
      <div class="stats_row">
        <div class="stat_card">
          <div class="stat_value">{{ completedTasks.length }}</div>
          <div class="stat_label">Выполнено заданий</div>
        </div>
        <div class="stat_card">
          <div class="stat_value">{{ totalPoints }}</div>
          <div class="stat_label">Суммарные баллы</div>
        </div>
        <div class="stat_card">
          <div class="stat_value">{{ averageGrade }}</div>
          <div class="stat_label">Средний балл</div>
        </div>
      </div>

      <!-- completed assignments -->
      <div class="card_assignments">
        <div class="card_header">
          <div>
            <span class="card_title">Выполненные задания</span>
            <p class="card_subtitle">Задания с выставленными оценками</p>
          </div>
        </div>
        <div v-if="completedTasks.length" class="grades_list">
          <div v-for="item in completedTasks" :key="item.id" class="grade_item">
            <div class="grade_main">
              <div class="grade_title">{{ item.title }}</div>
              <div class="grade_date">{{ formatDate(item.deadline) }}</div>
            </div>
            <div class="points_badge">+{{ item.exp }}</div>
          </div>
        </div>
        <div v-else class="empty_state">Выполненных заданий пока нет</div>
      </div>
    </div>
  </main>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import ProfileHero from '@/components/profile/ProfileHero.vue'
import { useTasksStore } from '@/stores/tasks_store.ts'

defineOptions({ name: 'ProfilePage' })

const tasksStore = useTasksStore()

onMounted(() => {
  tasksStore.fetchMyTasks()
})

const completedTasks = computed(function () {
  return tasksStore.myTasks.filter((t) => t.status === 'accepted')
})

const totalPoints = computed(function () {
  return completedTasks.value.reduce(function (sum, item) {
    return sum + item.exp
  }, 0)
})

const averageGrade = computed(function () {
  if (!completedTasks.value.length) return 0
  return Math.round(totalPoints.value / completedTasks.value.length)
})

function formatDate(str: string): string {
  return new Date(str).toLocaleDateString('ru-RU', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
  })
}
</script>

<style scoped>
main {
  box-sizing: border-box;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: rgb(244, 243, 250);
  min-height: 100vh;
}

.main_contents {
  padding-top: calc(100px + 70px);
  padding-bottom: 48px;
  width: 1000px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* cards */

.card {
  background-color: white;
  border: none;
  border-radius: 16px;
  box-shadow: 0px 0px 15px 0px rgba(0, 0, 0, 0.1);
  padding-block: 24px;
  padding-inline: 24px;
}

.card_assignments {
  background-color: white;
  border: none;
  border-radius: 16px;
  box-shadow: 0px 0px 15px 0px rgba(0, 0, 0, 0.1);
  padding-block: 24px;
  padding-inline: 24px;
}

/* stats */

.stats_row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.stat_card {
  background-color: white;
  border: none;
  border-radius: 16px;
  box-shadow: 0px 0px 15px 0px rgba(0, 0, 0, 0.1);
  padding: 20px 24px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.stat_value {
  font-family: Nagel;
  font-size: 2rem;
  color: rgb(160, 125, 180);
  line-height: 1;
}

.stat_label {
  font-family: Nagel;
  font-size: 13px;
  color: rgb(150, 150, 150);
}

/* completed assignments */

.card_header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
}

.card_title {
  font-family: Nagel;
  font-size: 18px;
  color: rgb(65, 65, 65);
  display: block;
  margin-bottom: 4px;
}

.card_subtitle {
  font-family: Nagel;
  font-size: 13px;
  color: rgb(150, 150, 150);
  margin: 0;
}

.grades_list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.grade_item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  padding: 14px 16px;
  border: none;
  border-radius: 12px;
  background-color: rgb(244, 243, 250);
}

.grade_main {
  flex: 1;
}

.grade_title {
  font-family: Nagel;
  font-size: 14px;
  color: rgb(65, 65, 65);
  margin-bottom: 4px;
}

.grade_date {
  font-family: Nagel;
  font-size: 12px;
  color: rgb(150, 150, 150);
}

.points_badge {
  padding: 8px 14px;
  border: none;
  border-radius: 12px;
  background-color: rgb(160, 125, 180);
  font-family: Nagel;
  font-size: 16px;
  color: white;
  flex-shrink: 0;
}

.empty_state {
  padding: 32px 16px;
  text-align: center;
  font-family: Nagel;
  color: rgb(150, 150, 150);
  font-size: 14px;
}

/* responsive */

@media screen and (max-width: 1050px) {
  main {
    padding-inline: 16px;
  }

  .main_contents {
    width: 100%;
  }
}

@media screen and (max-width: 540px) {
  .main_contents {
    padding-top: 70px;
  }

  .stats_row {
    grid-template-columns: 1fr 1fr;
  }

  .card {
    padding-inline: 12px;
  }
}
</style>
