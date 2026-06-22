<template>
  <main>
    <div class="main_contents page_enter">
      <div v-if="!submission || !task" class="card">
        <div class="empty_state">Сдача не найдена</div>
      </div>
      <div v-else-if="submission.status !== 'pending'" class="card">
        <div class="empty_state">Это задание уже проверено</div>
      </div>

      <template v-else>
        <!-- hero -->
        <div class="page_hero">
          <button type="button" class="back_btn" @click="router.push('/moderator/tasks')">
            <BackArrowIcon class="back_icon" />
          </button>
          <div class="hero_title_group">
            <h1 class="page_title">{{ task.title }}</h1>
            <span class="submitter_email">{{ submission.user_email }}</span>
          </div>
          <div class="points_pill">{{ task.exp }} баллов</div>
        </div>

        <div class="card">
          <span class="card_title">Письменный ответ</span>
          <p class="answer_text">{{ submission.content || 'Без письменного ответа' }}</p>
        </div>

        <div class="card">
          <span class="card_title">Файл ответа</span>
          <a v-if="submission.file" :href="submission.file.url" target="_blank" class="file_item">
            {{ submission.file.name }}
          </a>
          <p v-else class="muted_text">Файла нет</p>
        </div>

        <div class="card">
          <span class="card_title">Комментарий к проверке</span>
          <textarea
            v-model="comment"
            class="comment_input"
            placeholder="Комментарий для участника..."
            rows="3"
          ></textarea>
        </div>

        <div class="review_actions">
          <button
            type="button"
            class="action_btn_accept"
            :disabled="!isCommentValid"
            @click="handleReview('accepted')"
          >
            Принять
          </button>
          <button
            type="button"
            class="action_btn_reject"
            :disabled="!isCommentValid"
            @click="handleReview('rejected')"
          >
            Отклонить
          </button>
        </div>
        <p v-if="reviewError" class="review_error">{{ reviewError }}</p>
      </template>
    </div>
  </main>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useTasksStore } from '@/stores/tasks_store.ts'
import BackArrowIcon from '@/assets/icons/backarrow.svg'

defineOptions({ name: 'TaskReviewPage' })

const route = useRoute()
const router = useRouter()
const tasksStore = useTasksStore()

onMounted(() => {
  tasksStore.fetchMyTasks()
  tasksStore.fetchPendingReview()
})

const submissionId = route.params.id as string
const submission = computed(() => tasksStore.pendingReview.find((s) => s.id === submissionId))
const task = computed(() => tasksStore.myTasks.find((t) => t.id === submission.value?.task_id))

const comment = ref('')
const reviewError = ref('')

const isCommentValid = computed(() => comment.value.trim().length > 0)

async function handleReview(decision: 'accepted' | 'rejected'): Promise<void> {
  if (!submission.value) return
  reviewError.value = ''

  const action = decision === 'accepted' ? tasksStore.acceptSubmission : tasksStore.rejectSubmission
  const result = await action(submission.value.id, comment.value)
  if (result.success) router.push('/moderator/tasks')
  else reviewError.value = 'Не удалось оценить задание'
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
  box-shadow: 0px 0px 15px 0px rgba(0, 0, 0, 0.1);
}

.hero_title_group {
  flex: 1;
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
  box-shadow: 0px 0px 15px 0px rgba(0, 0, 0, 0.1);
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

.file_item {
  display: block;
  padding: 10px 14px;
  border: none;
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

.action_btn_accept {
  appearance: none;
  flex: 1;
  border: none;
  border-radius: 10px;
  padding: 14px 28px;
  font-family: Nagel;
  font-size: 15px;
  cursor: pointer;
  transition: 0.2s background-color;
  background-color: rgb(22, 163, 74);
  color: white;
}

.action_btn_accept:hover:not(:disabled) {
  background-color: rgb(18, 138, 63);
}

.action_btn_reject {
  appearance: none;
  flex: 1;
  border: none;
  border-radius: 10px;
  padding: 14px 28px;
  font-family: Nagel;
  font-size: 15px;
  cursor: pointer;
  transition: 0.2s background-color;
  background-color: rgb(204, 63, 75);
  color: white;
}

.action_btn_reject:hover:not(:disabled) {
  background-color: rgb(180, 50, 62);
}

.action_btn_accept:disabled,
.action_btn_reject:disabled {
  opacity: 0.4;
  cursor: default;
}

.review_error {
  font-family: Nagel;
  font-size: 13px;
  color: rgb(204, 63, 75);
  margin: 0;
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

  .review_actions {
    flex-direction: column;
  }
}
</style>
