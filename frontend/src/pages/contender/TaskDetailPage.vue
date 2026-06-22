<template>
  <main>
    <div class="main_contents page_enter">
      <div v-if="!task" class="card">
        <div class="empty_state">Задание не найдено</div>
      </div>

      <template v-else>
        <!-- hero -->
        <div class="page_hero">
          <button type="button" class="back_btn" @click="router.back()">
            <BackArrowIcon class="back_icon" />
          </button>
          <div class="hero_title_group">
            <h1 class="page_title">{{ task.title }}</h1>
            <span class="status_chip" :class="statusChip(status)">
              {{ statusLabel(status) }}
            </span>
          </div>
          <div class="points_pill">{{ task.exp }} баллов</div>
        </div>

        <div v-if="isDeletedAccount" class="deleted_note">
          Восстановите аккаунт перед отправкой
        </div>

        <div v-else-if="status === 'rejected'" class="rejected_note">
          Задание отклонено администратором. Вы можете изменить ответ и отправить его повторно.
        </div>

        <div v-if="currentSubmission?.admin_comment" class="card">
          <span class="card_title">Комментарий проверяющего</span>
          <p class="description_text">{{ currentSubmission.admin_comment }}</p>
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

        <!-- file (backend allows exactly one per submission) -->
        <div class="card">
          <span class="card_title">Файл ответа</span>

          <a
            v-if="!isEditable && currentSubmission?.file"
            :href="currentSubmission.file.url"
            target="_blank"
            class="file_name"
          >
            {{ currentSubmission.file.name }}
          </a>
          <p v-else-if="!isEditable" class="muted_text">Файла нет</p>

          <template v-else>
            <div v-if="selectedFile" class="file_item">
              <span class="file_name">{{ selectedFile.name }}</span>
              <button type="button" class="file_remove_btn" @click="selectedFile = null">
                Убрать
              </button>
            </div>
            <label v-else class="upload_btn">
              <span>Загрузить файл</span>
              <input type="file" hidden @change="handleFileChange" />
            </label>
          </template>
        </div>

        <!-- submit -->
        <button
          v-if="isEditable"
          type="button"
          class="submit_btn"
          :disabled="!answerInput.trim()"
          @click="handleSubmit"
        >
          {{ status === 'rejected' ? 'Отправить повторно' : 'Отправить ответ' }}
        </button>
        <p v-if="submitError" class="submit_error">{{ submitError }}</p>
      </template>
    </div>
  </main>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useTasksStore } from '@/stores/tasks_store.ts'
import { useAuthStore } from '@/stores/auth_store.ts'
import { formatDateLong as formatDate, isExpired, statusChip, statusLabel } from '@/utils/tasks.ts'
import BackArrowIcon from '@/assets/icons/backarrow.svg'

defineOptions({ name: 'TaskDetailPage' })

const route = useRoute()
const router = useRouter()
const tasksStore = useTasksStore()
const authStore = useAuthStore()

const taskId = route.params.id as string

onMounted(async () => {
  await Promise.all([tasksStore.fetchMyTasks(), tasksStore.fetchMySubmissions()])

  // a task can still be in the cached list with status "available" after its deadline
  // passed (the list just hasn't been refetched yet) — treat it as gone, same as a
  // task that was never assigned to this user at all
  if (!task.value || (status.value === 'available' && isExpired(task.value.deadline))) {
    router.replace({ name: 'not-found' })
  }
})

const task = computed(() => tasksStore.myTasks.find((t) => t.id === taskId))
const currentSubmission = computed(() => tasksStore.mySubmissionForTask(taskId))
const status = computed(() => currentSubmission.value?.status ?? 'available')
const isDeletedAccount = computed(
  () => authStore.role === 'member' && authStore.userStatus === 'deleted',
)
const isEditable = computed(
  () =>
    authStore.role === 'member' &&
    !isDeletedAccount.value &&
    (status.value === 'available' || status.value === 'rejected'),
)

// Pre-fill with the previous attempt's text when resubmitting after a rejection, so the
// user isn't retyping from scratch. The previous file can't be carried over the same way
// (no way to turn a stored URL back into a File object for re-upload), so that starts empty.
const answerInput = ref('')
watch(currentSubmission, (sub) => {
  if (sub) answerInput.value = sub.content
})
const selectedFile = ref<File | null>(null)
const submitError = ref('')

function handleFileChange(e: Event): void {
  const input = e.target as HTMLInputElement
  selectedFile.value = input.files?.[0] ?? null
}

async function handleSubmit(): Promise<void> {
  if (!task.value) return
  submitError.value = ''

  const result = await tasksStore.createSubmission(
    task.value.id,
    answerInput.value,
    selectedFile.value,
  )

  router.push('/tasks')

  if (!result.success) submitError.value = result.error
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
  flex-shrink: 0;
  border: none;
  background: none;
  padding: 0;
  display: flex;
  align-items: center;
  cursor: pointer;
  color: rgb(160, 125, 180);
  transition: color 0.2s;
}

.back_btn:hover {
  color: rgb(140, 105, 160);
}

.back_icon {
  width: 24px;
  height: 24px;
  transform: rotate(180deg);
}

/* hero */

.page_hero {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 28px 32px;
  background-color: white;
  border: none;
  border-radius: 16px;
  box-shadow: 0px 0px 15px 0px rgb(0, 0, 0, 0.1);
}

.hero_title_group {
  flex: 1;
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
  border: none;
  border-radius: 999px;
  background-color: rgb(160, 125, 180);
  font-family: Nagel;
  font-size: 14px;
  color: white;
}

/* cards */

.card {
  background-color: white;
  border: none;
  border-radius: 16px;
  box-shadow: 0px 0px 15px 0px rgb(0, 0, 0, 0.1);
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

.file_item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  padding: 10px 14px;
  border: none;
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

.submit_error {
  font-family: Nagel;
  font-size: 13px;
  color: rgb(204, 63, 75);
  margin: 0;
}

/* status chip (reused naming/colors from TasksPage) */

.status_chip {
  display: inline-block;
  padding: 4px 10px;
  border: none;
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
  border: none;
  border-radius: 12px;
  background-color: rgba(204, 63, 75, 0.08);
  font-family: Nagel;
  font-size: 14px;
  color: rgb(204, 63, 75);
}

/* deleted account note */

.deleted_note {
  padding: 14px 18px;
  border: none;
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

  .page_hero {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
}
</style>
