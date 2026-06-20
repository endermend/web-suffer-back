<template>
  <main>
    <div class="main_contents page_enter">
      <div class="page_hero">
        <button type="button" class="back_btn" @click="router.push('/moderator/tasks')">
          <BackArrowIcon class="back_icon" />
        </button>
        <div class="hero_title_group">
          <h1 class="page_title">
            {{ isEditMode ? 'Редактирование задания' : 'Создание задания' }}
          </h1>
          <p class="page_subtitle">
            {{
              isEditMode
                ? 'Измените данные существующего задания'
                : 'Заполните поля, чтобы опубликовать новое задание'
            }}
          </p>
        </div>
      </div>

      <div v-if="isEditMode && !task" class="card">
        <div class="empty_state">Задание не найдено</div>
      </div>

      <div v-else class="card">
        <form class="create_form" @submit.prevent="handleSubmit" novalidate>
          <div class="form_field">
            <label class="form_label">Название</label>
            <input v-model="form.title" class="form_input" required />
          </div>
          <div class="form_field">
            <label class="form_label">Описание</label>
            <textarea v-model="form.description" class="form_input" rows="4" required></textarea>
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
          <button type="submit" class="submit_btn" :disabled="!isFormValid">
            {{ isEditMode ? 'Сохранить изменения' : 'Создать задание' }}
          </button>
          <p v-if="submitError" class="create_error">{{ submitError }}</p>
        </form>
      </div>
    </div>
  </main>
</template>

<script setup lang="ts">
import { reactive, computed, ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useTasksStore } from '@/stores/tasks_store.ts'
import { toDatetimeLocalInput } from '@/utils/tasks.ts'
import BackArrowIcon from '@/assets/icons/backarrow.svg'

defineOptions({ name: 'CreateTaskPage' })

const route = useRoute()
const router = useRouter()
const tasksStore = useTasksStore()

const taskId = route.params.id as string | undefined
const isEditMode = computed(() => !!taskId)
const task = computed(() => (taskId ? tasksStore.myTasks.find((t) => t.id === taskId) : undefined))

const form = reactive({
  title: '',
  description: '',
  deadline: '',
  exp: 10,
  // not shown in the form — preserved from the existing task on edit, defaults to 0 on create
  money: 0,
})

const submitError = ref('')

// Mirrors TaskDetailPage's submit-button gating: stay disabled (gray) until every
// required field actually holds a usable value, instead of relying on native HTML5
// validation popups (the form has novalidate so those never show).
const isFormValid = computed(() => {
  const exp = Number(form.exp)
  return (
    form.title.trim().length > 0 &&
    form.description.trim().length > 0 &&
    !!form.deadline &&
    Number.isFinite(exp) &&
    exp > 0
  )
})

onMounted(async () => {
  if (!taskId) return

  await tasksStore.fetchMyTasks()
  if (!task.value) return

  form.title = task.value.title
  form.description = task.value.description
  form.deadline = toDatetimeLocalInput(task.value.deadline)
  form.exp = task.value.exp
  form.money = task.value.money
})

async function handleSubmit(): Promise<void> {
  submitError.value = ''
  const result = await tasksStore.saveTask({ task_id: taskId, ...form })
  if (!result.success) {
    submitError.value = isEditMode.value
      ? 'Не удалось сохранить изменения'
      : 'Не удалось создать задание'
    return
  }
  router.push('/moderator/tasks')
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
  border-radius: 16px;
  box-shadow: 0px 0px 15px 0px rgb(0, 0, 0, 0.2);
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
  box-shadow: 0px 0px 15px 0px rgb(0, 0, 0, 0.2);
  padding: 24px;
}

/* form */

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

.submit_btn:hover:not(:disabled) {
  background-color: rgb(140, 105, 160);
}

.submit_btn:disabled {
  opacity: 0.4;
  cursor: default;
}

.create_error {
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

  .form_row {
    flex-direction: column;
  }
}
</style>
