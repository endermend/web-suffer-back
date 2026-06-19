<template>
  <main>
    <div class="main_contents">
      <!-- hero -->
      <div class="page_hero">
        <div>
          <button type="button" class="back_btn" @click="router.push('/tasks')">← Назад</button>
          <h1 class="page_title">Все доступные задания</h1>
          <p class="page_subtitle">Задания, которые можно взять прямо сейчас</p>
        </div>
      </div>

      <div class="card">
        <div v-if="availableTasks.length" class="assignment_list">
          <div
            v-for="item in availableTasks"
            :key="item.id"
            class="assignment_item"
            @click="router.push(`/tasks/${item.id}`)"
          >
            <div class="assignment_main">
              <div class="assignment_title">{{ item.title }}</div>
              <div class="assignment_description">{{ item.description }}</div>
            </div>
            <div class="assignment_side">
              <div class="deadline_label">Дедлайн</div>
              <div class="deadline_date">{{ formatDate(item.deadline) }}</div>
              <div class="points_label">{{ item.points }} баллов</div>
            </div>
          </div>
        </div>
        <div v-else class="empty_state">Доступных заданий нет</div>
      </div>
    </div>
  </main>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useTasksStore } from '@/stores/tasks_store.ts'
import { formatDateShort as formatDate } from '@/utils/tasks.ts'

defineOptions({ name: 'AllTasksPage' })

const router = useRouter()
const tasksStore = useTasksStore()

const availableTasks = computed(() => tasksStore.availableTasks)
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

/* hero */

.page_hero {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 28px 32px;
  background-color: white;
  border-radius: 16px;
  margin-top: 32px;
  box-shadow: 0px 0px 15px 0px rgb(211, 211, 211);
}

.back_btn {
  appearance: none;
  border: none;
  background: none;
  padding: 0;
  margin-bottom: 10px;
  font-family: Nagel;
  font-size: 14px;
  color: rgb(160, 125, 180);
  cursor: pointer;
}

.back_btn:hover {
  text-decoration: underline;
}

.page_title {
  font-family: Nagel;
  font-size: 2rem;
  color: rgb(65, 65, 65);
  margin: 0 0 6px;
}

.page_subtitle {
  font-family: Nagel;
  font-size: 14px;
  color: rgb(150, 150, 150);
  margin: 0;
}

/* card */

.card {
  background-color: white;
  border-radius: 16px;
  box-shadow: 0px 0px 15px 0px rgb(211, 211, 211);
  padding: 24px;
}

/* assignment list */

.assignment_list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.assignment_item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  padding: 16px 18px;
  border-radius: 12px;
  background-color: rgb(244, 243, 250);
  cursor: pointer;
  transition: 0.2s background-color;
}

.assignment_item:hover {
  background-color: rgb(235, 230, 245);
}

.assignment_main {
  min-width: 0;
}

.assignment_title {
  font-family: Nagel;
  font-size: 15px;
  color: rgb(65, 65, 65);
  margin-bottom: 4px;
}

.assignment_description {
  font-family: Nagel;
  font-size: 13px;
  color: rgb(150, 150, 150);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.assignment_side {
  text-align: right;
  flex-shrink: 0;
}

.deadline_label {
  font-family: Nagel;
  font-size: 12px;
  color: rgb(150, 150, 150);
  margin-bottom: 2px;
}

.deadline_date {
  font-family: Nagel;
  font-size: 13px;
  color: rgb(204, 63, 75);
}

.points_label {
  font-family: Nagel;
  font-size: 12px;
  color: rgb(160, 125, 180);
  margin-top: 2px;
}

/* states */

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
    padding-inline: 32px;
  }

  .main_contents {
    width: 100%;
  }
}

@media screen and (max-width: 540px) {
  .main_contents {
    padding-top: 70px;
  }

  .assignment_item {
    flex-direction: column;
    align-items: flex-start;
  }

  .assignment_side {
    text-align: left;
  }
}
</style>
