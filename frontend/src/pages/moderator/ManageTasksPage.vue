<template>
  <main>
    <div class="main_contents page_enter">
      <div class="page_hero">
        <h1 class="page_title">Управление заданиями</h1>
        <p class="page_subtitle">Создание заданий и проверка ответов участников</p>
      </div>

      <!-- tasks -->
      <div class="card">
        <div class="card_header">
          <span class="card_title">Задания</span>
          <button type="button" class="create_btn" @click="router.push('/moderator/tasks/create')">
            Создать задание
          </button>
        </div>

        <div v-if="availableTasks.length" class="existing_list">
          <button
            v-for="item in availableTasks"
            :key="item.id"
            type="button"
            class="existing_item"
            @click="router.push(`/moderator/tasks/${item.id}/edit`)"
          >
            <span class="existing_title">{{ item.title }}</span>
            <span class="existing_deadline">{{ formatDate(item.deadline) }}</span>
          </button>
        </div>
        <div v-else class="empty_state">Нет доступных для пользователей заданий</div>
      </div>

      <!-- review -->
      <div class="card">
        <span class="card_title">Проверка выполненных заданий</span>
        <div v-if="pendingSubmissions.length" class="review_list">
          <div v-for="item in pendingSubmissions" :key="item.submission.id" class="review_item">
            <div class="review_main">
              <span class="review_title">{{ item.task?.title }}</span>
              <span class="review_submitter">{{ item.submission.user_email }}</span>
            </div>
            <button
              type="button"
              class="open_review_btn"
              @click="router.push(`/moderator/submissions/${item.submission.id}/review`)"
            >
              Открыть
            </button>
          </div>
        </div>
        <div v-else class="empty_state">Нет заданий, ожидающих проверки</div>
      </div>
    </div>
  </main>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useTasksStore } from '@/stores/tasks_store.ts'
import { formatDateShort as formatDate } from '@/utils/tasks.ts'

defineOptions({ name: 'ManageTasksPage' })

const router = useRouter()
const tasksStore = useTasksStore()

onMounted(() => {
  tasksStore.fetchMyTasks()
  tasksStore.fetchPendingReview()
})

// A moderator never submits, so every task they fetch shows up here regardless of status.
const availableTasks = computed(() => tasksStore.myTasks)

// The submissions endpoint doesn't include the task title, so each pending row is
// cross-referenced against the task list fetched above.
const pendingSubmissions = computed(() =>
  tasksStore.pendingSubmissions.map((submission) => ({
    submission,
    task: tasksStore.myTasks.find((t) => t.id === submission.task_id),
  })),
)
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
  margin-top: 32px;
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

/* cards */

.card {
  background-color: white;
  border-radius: 16px;
  box-shadow: 0px 0px 15px 0px rgba(0, 0, 0, 0.1);
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.card_title {
  font-family: Nagel;
  font-size: 18px;
  color: rgb(65, 65, 65);
}

.card_header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.create_btn {
  appearance: none;
  flex-shrink: 0;
  border: none;
  border-radius: 10px;
  padding: 10px 22px;
  font-family: Nagel;
  font-size: 14px;
  cursor: pointer;
  background-color: rgb(160, 125, 180);
  color: white;
  transition: 0.2s background-color;
}

.create_btn:hover {
  background-color: rgb(140, 105, 160);
}

/* existing tasks list */

.existing_list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.existing_item {
  appearance: none;
  width: 100%;
  box-sizing: border-box;
  border: none;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  padding: 10px 14px;
  border-radius: 10px;
  background-color: rgb(244, 243, 250);
  cursor: pointer;
  text-align: left;
  transition: 0.2s background-color;
}

.existing_item:hover {
  background-color: rgb(235, 230, 245);
}

.existing_title {
  font-family: Nagel;
  font-size: 14px;
  color: rgb(65, 65, 65);
}

.existing_deadline {
  font-family: Nagel;
  font-size: 12px;
  color: rgb(150, 150, 150);
  flex-shrink: 0;
}

/* review */

.review_list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.review_item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  border-radius: 12px;
  background-color: rgb(244, 243, 250);
}

.review_main {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.review_title {
  font-family: Nagel;
  font-size: 15px;
  color: rgb(65, 65, 65);
}

.review_submitter {
  font-family: Nagel;
  font-size: 12px;
  color: rgb(150, 150, 150);
}

.open_review_btn {
  appearance: none;
  flex-shrink: 0;
  border: none;
  border-radius: 10px;
  padding: 8px 18px;
  font-family: Nagel;
  font-size: 13px;
  cursor: pointer;
  background-color: rgb(160, 125, 180);
  color: white;
  transition: 0.2s background-color;
}

.open_review_btn:hover {
  background-color: rgb(140, 105, 160);
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

  .card_header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .review_item {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
