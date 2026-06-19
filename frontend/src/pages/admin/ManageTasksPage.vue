<template>
  <main>
    <div class="main_contents">
      <div class="page_hero">
        <h1 class="page_title">Управление заданиями</h1>
        <p class="page_subtitle">Создание заданий и проверка ответов участников</p>
      </div>

      <!-- create task -->
      <div class="card">
        <span class="card_title">Создать задание</span>
        <form class="create_form" @submit.prevent="handleCreate">
          <div class="form_field">
            <label class="form_label">Название</label>
            <input v-model="form.title" class="form_input" required />
          </div>
          <div class="form_field">
            <label class="form_label">Описание</label>
            <textarea v-model="form.description" class="form_input" rows="3" required></textarea>
          </div>
          <div class="form_row">
            <div class="form_field">
              <label class="form_label">Дедлайн</label>
              <input v-model="form.deadline" type="datetime-local" class="form_input" required />
            </div>
            <div class="form_field">
              <label class="form_label">Баллы</label>
              <input v-model.number="form.exp" type="number" min="1" class="form_input" required />
            </div>
          </div>
          <button type="submit" class="submit_btn">Создать задание</button>
          <p v-if="createError" class="create_error">{{ createError }}</p>
        </form>

        <div v-if="availableTasks.length" class="existing_list">
          <div v-for="item in availableTasks" :key="item.id" class="existing_item">
            <span class="existing_title">{{ item.title }}</span>
            <span class="existing_deadline">{{ formatDate(item.deadline) }}</span>
          </div>
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
              @click="router.push(`/admin/submissions/${item.submission.id}/review`)"
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
import { reactive, computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useTasksStore } from '@/stores/tasks_store.ts'
import { formatDateShort as formatDate } from '@/utils/tasks.ts'

defineOptions({ name: 'ManageTasksPage' })

const router = useRouter()
const tasksStore = useTasksStore()

const form = reactive({
  title: '',
  description: '',
  deadline: '',
  exp: 10,
  // not shown in the create form yet — see types/tasks.ts for why the field still exists
  money: 0,
})

const createError = ref('')

async function handleCreate(): Promise<void> {
  createError.value = ''
  const result = await tasksStore.createTask({ ...form })
  if (!result.success) {
    createError.value = 'Не удалось создать задание'
    return
  }
  form.title = ''
  form.description = ''
  form.deadline = ''
  form.exp = 10
}

// Task templates have no status of their own anymore, so every one of them belongs here.
const availableTasks = computed(() => tasksStore.tasks)

// Submissions are their own entities now (one task can have several pending submissions,
// one per user), so each pending row is joined with its task for display.
const pendingSubmissions = computed(() =>
  tasksStore.pendingSubmissions.map((submission) => ({
    submission,
    task: tasksStore.tasks.find((t) => t.id === submission.task_id),
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
  box-shadow: 0px 0px 15px 0px rgb(0, 0, 0, 0.2);
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

/* create form */

.create_form {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.form_row {
  display: flex;
  gap: 14px;
}

.form_row .form_field {
  flex: 1;
}

.form_field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form_label {
  font-family: Nagel;
  font-size: 13px;
  color: rgb(150, 150, 150);
}

.form_input {
  appearance: none;
  box-sizing: border-box;
  width: 100%;
  border: thin solid rgb(210, 208, 220);
  border-radius: 10px;
  padding: 10px 14px;
  font-family: Nagel;
  font-size: 14px;
  color: rgb(65, 65, 65);
  background-color: white;
  outline: none;
  resize: vertical;
  transition: 0.2s border-color;
}

.form_input:focus {
  border-color: rgb(160, 125, 180);
}

.submit_btn {
  appearance: none;
  align-self: flex-start;
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

.submit_btn:hover {
  background-color: rgb(140, 105, 160);
}

.create_error {
  font-family: Nagel;
  font-size: 13px;
  color: rgb(204, 63, 75);
  margin: 0;
}

/* existing tasks list */

.existing_list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding-top: 8px;
  border-top: thin solid rgb(230, 228, 240);
}

.existing_item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  padding: 10px 14px;
  border-radius: 10px;
  background-color: rgb(244, 243, 250);
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

  .form_row {
    flex-direction: column;
  }

  .review_item {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
