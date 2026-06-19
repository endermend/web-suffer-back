<template>
  <main>
    <div class="main_contents">
      <button type="button" class="back_btn" @click="router.push('/admin/tasks')">← Назад</button>

      <div v-if="!task" class="card">
        <div class="empty_state">Сдача не найдена</div>
      </div>
      <div v-else-if="task.status !== 'submitted'" class="card">
        <div class="empty_state">Это задание уже проверено</div>
      </div>

      <template v-else>
        <!-- hero -->
        <div class="page_hero">
          <div>
            <h1 class="page_title">{{ task.title }}</h1>
            <span class="submitter_email">{{ task.submitted_by }}</span>
          </div>
          <div class="points_pill">{{ task.points }} баллов</div>
        </div>

        <div class="card">
          <span class="card_title">Письменный ответ</span>
          <p class="answer_text">{{ task.answer || 'Без письменного ответа' }}</p>
        </div>

        <div class="card">
          <span class="card_title">Файлы ответа</span>
          <div v-if="task.submission_files.length" class="file_list">
            <a
              v-for="file in task.submission_files"
              :key="file.id"
              :href="file.url"
              target="_blank"
              class="file_item"
            >
              {{ file.name }}
            </a>
          </div>
          <p v-else class="muted_text">Файлов нет</p>
        </div>

        <div class="card">
          <span class="card_title">Комментарий к проверке</span>
          <textarea
            v-model="comment"
            class="comment_input"
            placeholder="Комментарий для участника (необязательно)..."
            rows="3"
          ></textarea>
        </div>

        <div class="review_actions">
          <button type="button" class="action_btn action_btn_accept" @click="handleAccept">
            Принять
          </button>
          <button type="button" class="action_btn action_btn_reject" @click="handleReject">
            Отклонить
          </button>
        </div>
      </template>
    </div>
  </main>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useTasksStore } from '@/stores/tasks_store.ts'

defineOptions({ name: 'TaskReviewPage' })

const route = useRoute()
const router = useRouter()
const tasksStore = useTasksStore()

const taskId = Number(route.params.id)
const task = computed(() => tasksStore.tasks.find((t) => t.id === taskId))

const comment = ref('')

function handleAccept(): void {
  if (!task.value) return
  tasksStore.gradeTask(task.value.id, comment.value)
  router.push('/admin/tasks')
}

function handleReject(): void {
  if (!task.value) return
  tasksStore.rejectTask(task.value.id, comment.value)
  router.push('/admin/tasks')
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
  padding-top: calc(100px + 100px);
  padding-bottom: 48px;
  width: 760px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.back_btn {
  appearance: none;
  align-self: flex-start;
  border: none;
  background: none;
  padding: 0;
  font-family: Nagel;
  font-size: 14px;
  color: rgb(160, 125, 180);
  cursor: pointer;
}

.back_btn:hover {
  text-decoration: underline;
}

/* hero */

.page_hero {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 28px 32px;
  background-color: white;
  border-radius: 16px;
  box-shadow: 0px 0px 15px 0px rgb(211, 211, 211);
}

.page_title {
  font-family: Nagel;
  font-size: 1.6rem;
  color: rgb(65, 65, 65);
  margin: 0 0 6px;
}

.submitter_email {
  font-family: Nagel;
  font-size: 14px;
  color: rgb(150, 150, 150);
}

.points_pill {
  flex-shrink: 0;
  padding: 8px 16px;
  border-radius: 999px;
  background-color: rgb(160, 125, 180);
  font-family: Nagel;
  font-size: 14px;
  color: white;
}

/* cards */

.card {
  background-color: white;
  border-radius: 16px;
  box-shadow: 0px 0px 15px 0px rgb(211, 211, 211);
  padding: 24px;
}

.card_title {
  font-family: Nagel;
  font-size: 16px;
  color: rgb(65, 65, 65);
  display: block;
  margin-bottom: 12px;
}

.answer_text {
  font-family: Nagel;
  font-size: 14px;
  color: rgb(65, 65, 65);
  white-space: pre-wrap;
  margin: 0;
}

.muted_text {
  font-family: Nagel;
  font-size: 13px;
  color: rgb(150, 150, 150);
  margin: 0;
}

/* comment */

.comment_input {
  width: 100%;
  box-sizing: border-box;
  resize: vertical;
  border: thin solid rgb(210, 208, 220);
  border-radius: 10px;
  padding: 12px 14px;
  font-family: Nagel;
  font-size: 14px;
  color: rgb(65, 65, 65);
  outline: none;
  transition: 0.2s border-color;
}

.comment_input:focus {
  border-color: rgb(160, 125, 180);
}

/* files */

.file_list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.file_item {
  display: block;
  padding: 10px 14px;
  border-radius: 10px;
  background-color: rgb(244, 243, 250);
  font-family: Nagel;
  font-size: 14px;
  color: rgb(65, 65, 65);
  text-decoration: none;
}

.file_item:hover {
  background-color: rgb(235, 230, 245);
}

/* actions */

.review_actions {
  display: flex;
  gap: 12px;
}

.action_btn {
  appearance: none;
  flex: 1;
  border: none;
  border-radius: 10px;
  padding: 14px 28px;
  font-family: Nagel;
  font-size: 15px;
  cursor: pointer;
  transition: 0.2s background-color;
}

.action_btn_accept {
  background-color: rgb(22, 163, 74);
  color: white;
}

.action_btn_accept:hover {
  background-color: rgb(18, 138, 63);
}

.action_btn_reject {
  background-color: rgb(204, 63, 75);
  color: white;
}

.action_btn_reject:hover {
  background-color: rgb(180, 50, 62);
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

  .page_hero {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .review_actions {
    flex-direction: column;
  }
}
</style>
