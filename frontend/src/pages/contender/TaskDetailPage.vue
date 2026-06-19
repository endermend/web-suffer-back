<template>
  <main>
    <div class="main_contents">
      <button type="button" class="back_btn" @click="router.back()">← Назад</button>

      <div v-if="!task" class="card">
        <div class="empty_state">Задание не найдено</div>
      </div>

      <template v-else>
        <!-- hero -->
        <div class="page_hero">
          <div>
            <h1 class="page_title">{{ task.title }}</h1>
            <span class="status_chip" :class="statusChip(task.status)">
              {{ statusLabel(task.status) }}
            </span>
          </div>
          <div class="points_pill">{{ task.points }} баллов</div>
        </div>

        <div v-if="task.status === 'rejected'" class="rejected_note">
          Задание отклонено администратором. Вы можете изменить ответ и отправить его повторно.
        </div>

        <div v-if="task.admin_comment" class="card">
          <span class="card_title">Комментарий проверяющего</span>
          <p class="description_text">{{ task.admin_comment }}</p>
        </div>

        <!-- deadline + description -->
        <div class="card">
          <span class="card_title">Дедлайн</span>
          <p class="deadline_date">{{ formatDate(task.deadline) }}</p>
        </div>

        <div class="card">
          <span class="card_title">Описание задания</span>
          <p class="description_text">{{ task.description }}</p>
        </div>

        <!-- answer -->
        <div class="card">
          <span class="card_title">Письменный ответ</span>
          <textarea
            v-model="answerInput"
            class="answer_input"
            :disabled="!isEditable"
            placeholder="Введите ответ на задание..."
            rows="5"
          ></textarea>
        </div>

        <!-- files -->
        <div class="card">
          <span class="card_title">Файлы ответа</span>
          <div v-if="task.submission_files.length" class="file_list">
            <div v-for="file in task.submission_files" :key="file.id" class="file_item">
              <a :href="file.url" target="_blank" class="file_name">{{ file.name }}</a>
              <button
                v-if="isEditable"
                type="button"
                class="file_remove_btn"
                @click="tasksStore.removeSubmissionFile(task.id, file.id)"
              >
                Удалить
              </button>
            </div>
          </div>
          <p v-else class="muted_text">Файлов пока нет</p>

          <label v-if="isEditable" class="upload_btn">
            <span>Загрузить файл</span>
            <input type="file" hidden multiple @change="handleFileUpload" />
          </label>
        </div>

        <!-- submit -->
        <button
          v-if="isEditable"
          type="button"
          class="submit_btn"
          :disabled="!answerInput.trim()"
          @click="handleSubmit"
        >
          {{ task.status === 'rejected' ? 'Отправить повторно' : 'Отправить ответ' }}
        </button>
      </template>
    </div>
  </main>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useTasksStore } from '@/stores/tasks_store.ts'
import { useAuthStore } from '@/stores/auth_store.ts'
import { formatDateLong as formatDate, statusChip, statusLabel } from '@/utils/tasks.ts'

defineOptions({ name: 'TaskDetailPage' })

const route = useRoute()
const router = useRouter()
const tasksStore = useTasksStore()
const authStore = useAuthStore()

const taskId = Number(route.params.id)
const task = computed(() => tasksStore.tasks.find((t) => t.id === taskId))
const isEditable = computed(
  () => task.value?.status === 'available' || task.value?.status === 'rejected',
)

const answerInput = ref(task.value?.answer ?? '')

function handleFileUpload(e: Event): void {
  if (!task.value) return
  const input = e.target as HTMLInputElement
  const files = input.files
  if (!files) return
  for (const file of Array.from(files)) {
    tasksStore.addSubmissionFile(task.value.id, file)
  }
  input.value = ''
}

function handleSubmit(): void {
  if (!task.value) return
  if (!confirm('Отправить ответ? После отправки изменить его будет нельзя.')) return
  tasksStore.updateAnswer(task.value.id, answerInput.value)
  tasksStore.submitTask(task.value.id, authStore.userEmail ?? '')
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
  margin: 0 0 10px;
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

.deadline_date {
  font-family: Nagel;
  font-size: 15px;
  color: rgb(204, 63, 75);
  margin: 0;
}

.description_text {
  font-family: Nagel;
  font-size: 14px;
  color: rgb(65, 65, 65);
  white-space: pre-wrap;
  margin: 0;
}

/* answer */

.answer_input {
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

.answer_input:focus {
  border-color: rgb(160, 125, 180);
}

.answer_input:disabled {
  background-color: rgb(244, 243, 250);
  color: rgb(150, 150, 150);
}

/* files */

.file_list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 14px;
}

.file_item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  padding: 10px 14px;
  border-radius: 10px;
  background-color: rgb(244, 243, 250);
}

.file_name {
  font-family: Nagel;
  font-size: 14px;
  color: rgb(65, 65, 65);
  text-decoration: none;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.file_name:hover {
  text-decoration: underline;
}

.file_remove_btn {
  appearance: none;
  flex-shrink: 0;
  border: none;
  background: none;
  font-family: Nagel;
  font-size: 12px;
  color: rgb(204, 63, 75);
  cursor: pointer;
}

.muted_text {
  font-family: Nagel;
  font-size: 13px;
  color: rgb(150, 150, 150);
  margin: 0 0 14px;
}

.upload_btn {
  display: inline-flex;
  appearance: none;
  border: thin solid rgb(210, 208, 220);
  border-radius: 10px;
  padding: 10px 18px;
  font-family: Nagel;
  font-size: 14px;
  cursor: pointer;
  background-color: white;
  color: rgb(65, 65, 65);
  transition: 0.2s background-color;
}

.upload_btn:hover {
  background-color: rgb(244, 243, 250);
}

/* submit */

.submit_btn {
  appearance: none;
  align-self: flex-start;
  border: none;
  border-radius: 10px;
  padding: 14px 28px;
  font-family: Nagel;
  font-size: 15px;
  cursor: pointer;
  background-color: rgb(160, 125, 180);
  color: white;
  transition: 0.2s background-color;
}

.submit_btn:hover:not(:disabled) {
  background-color: rgb(140, 105, 160);
}

.submit_btn:disabled {
  opacity: 0.4;
  cursor: default;
}

/* status chip (reused naming/colors from TasksPage) */

.status_chip {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 999px;
  font-family: Nagel;
  font-size: 12px;
}

.chip_assigned {
  background-color: rgba(160, 125, 180, 0.12);
  color: rgb(120, 80, 150);
}
.chip_submitted {
  background-color: rgba(202, 138, 4, 0.12);
  color: rgb(161, 100, 0);
}
.chip_graded {
  background-color: rgba(22, 163, 74, 0.12);
  color: rgb(22, 163, 74);
}
.chip_rejected {
  background-color: rgba(204, 63, 75, 0.12);
  color: rgb(204, 63, 75);
}

/* rejected note */

.rejected_note {
  padding: 14px 18px;
  border-radius: 12px;
  background-color: rgba(204, 63, 75, 0.08);
  font-family: Nagel;
  font-size: 14px;
  color: rgb(204, 63, 75);
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
}
</style>
