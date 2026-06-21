<template>
  <main>
    <div class="main_contents page_enter">
      <!-- hero -->
      <div class="page_hero">
        <div>
          <h1 class="page_title">Задания</h1>
          <p class="page_subtitle">Следите за дедлайнами и выполняйте задания вовремя</p>
        </div>
      </div>

      <!-- main grid -->
      <div class="tasks_grid">
        <!-- top row: the two anchor cards keep a fixed wide/narrow split -->
        <div class="grid_top">
          <!-- active assignments -->
          <div class="card">
            <div class="card_header">
              <div>
                <span class="card_title">Доступные задания</span>
                <p class="card_subtitle">Новые задания для выполнения</p>
              </div>
            </div>
            <div v-if="activeTasks.length" class="assignment_list">
              <div
                v-for="item in activeTasks"
                :key="item.id"
                class="assignment_item"
                @click="router.push(`/tasks/${item.id}`)"
              >
                <div class="assignment_main">
                  <div class="assignment_title">{{ item.title }}</div>
                </div>
                <div class="assignment_side">
                  <div class="deadline_date">Дедлайн {{ formatDate(item.deadline) }}</div>
                  <div class="points_label">{{ item.exp }} баллов</div>
                </div>
              </div>
            </div>
            <div v-else class="empty_state">Активных заданий нет</div>
            <button type="button" class="view_all_btn" @click="router.push('/tasks/all')">
              Перейти ко всем доступным
            </button>
          </div>

          <!-- progress -->
          <div class="card_progress">
            <div class="card_header">
              <div>
                <span class="card_title">Правильность</span>
                <p class="card_subtitle">Ошибочные задания можно пересдать</p>
              </div>
            </div>
            <div class="progress_circle_wrap">
              <div class="progress_circle" :style="{ '--progress': animatedProgress }">
                <span class="progress_inner">{{ animatedProgress }}%</span>
              </div>
            </div>
            <p class="progress_info">
              Правильно выполнено {{ completedCount }} из {{ totalCount }} заданий
            </p>
            <div class="progress_bar">
              <div class="progress_fill" :style="{ width: animatedProgress + '%' }"></div>
            </div>
          </div>
        </div>

        <div class="grid_bottom">
          <!-- recent grades -->
          <div class="card grades_card">
            <div class="card_header">
              <div>
                <span class="card_title">Последние выставленные баллы</span>
                <p class="card_subtitle">Недавно проверенные задания</p>
              </div>
            </div>
            <div v-if="recentCompleted.length" class="grades_list">
              <div v-for="item in recentCompleted" :key="item.id" class="grade_item">
                <div class="grade_main">
                  <div class="grade_title">{{ item.title }}</div>
                  <div class="grade_date">{{ formatDate(item.deadline) }}</div>
                </div>
                <div class="points_badge">+{{ item.exp }}</div>
              </div>
            </div>
            <div v-else class="empty_state">Оценок пока нет</div>
            <button
              type="button"
              class="view_all_btn grades_footer_btn"
              @click="router.push('/profile')"
            >
              Все выполненные
            </button>
          </div>

          <div class="grid_bottom_right">
            <!-- pending review -->
            <div class="card">
              <div class="card_header">
                <div>
                  <span class="card_title">Ожидают проверки</span>
                  <p class="card_subtitle">Работы на проверке</p>
                </div>
              </div>
              <div v-if="pendingTasks.length" class="pending_list">
                <div v-for="item in pendingTasks" :key="item.id" class="pending_item">
                  <div class="pending_title">{{ item.title }}</div>
                  <span class="status_chip chip_submitted">Проверяется</span>
                </div>
              </div>
              <div v-else class="ok_state">Все работы проверены</div>
            </div>

            <!-- rejected -->
            <div class="card">
              <div class="card_header">
                <div>
                  <span class="card_title">Отклонённые</span>
                  <p class="card_subtitle">Можно исправить и отправить повторно</p>
                </div>
              </div>
              <div v-if="rejectedTasks.length" class="pending_list">
                <div
                  v-for="item in rejectedTasks"
                  :key="item.id"
                  class="rejected_item"
                  @click="router.push(`/tasks/${item.id}`)"
                >
                  <div class="pending_title">{{ item.title }}</div>
                  <span class="status_chip chip_rejected">Отклонено</span>
                </div>
              </div>
              <div v-else class="ok_state">Отклонённых заданий нет</div>
            </div>
          </div>
        </div>
      </div>

      <!-- filters -->
      <div class="card filters_card">
        <div class="filters_row">
          <div class="filter_field">
            <label class="filter_label">Поиск</label>
            <input v-model="searchQuery" class="filter_input" placeholder="Название задания..." />
          </div>
          <div class="filter_field">
            <label class="filter_label">Дедлайн до</label>
            <input v-model="deadlineBefore" type="date" class="filter_input" />
          </div>
          <div class="filter_field">
            <label class="filter_label">Дедлайн после</label>
            <input v-model="deadlineAfter" type="date" class="filter_input" />
          </div>
          <div class="filter_field">
            <label class="filter_label">Статус</label>
            <select v-model="statusFilter" class="filter_input">
              <option value="">Все статусы</option>
              <option value="available">Доступно</option>
              <option value="pending">Проверяется</option>
              <option value="accepted">Проверено</option>
              <option value="rejected">Отклонено</option>
            </select>
          </div>
          <div class="filter_actions">
            <button class="filter_btn filter_btn_primary" @click="applyFilters">Применить</button>
            <button
              v-if="searchQuery || deadlineBefore || deadlineAfter || statusFilter"
              class="filter_btn"
              @click="clearFilters"
            >
              Сбросить
            </button>
          </div>
        </div>
      </div>

      <!-- tasks table -->
      <div class="card table_card">
        <div v-if="paginatedTasks.length === 0" class="empty_state">Заданий не найдено</div>
        <template v-else>
          <span class="card_title">Список заданий ({{ filteredTasks.length }})</span>
          <div class="table_wrap">
            <table class="tasks_table">
              <thead>
                <tr>
                  <th>Задание</th>
                  <th>Дедлайн</th>
                  <th>Статус</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="item in paginatedTasks"
                  :key="item.id"
                  class="task_row"
                  @click="router.push(`/tasks/${item.id}`)"
                >
                  <td>{{ item.title }}</td>
                  <td>{{ formatDate(item.deadline) }}</td>
                  <td>
                    <span class="status_chip" :class="statusChip(item.status)">
                      {{ statusLabel(item.status) }}
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <div class="pagination_bar">
            <span class="pagination_info">Страница {{ currentPage }} из {{ totalPages }}</span>
            <div class="pagination_btns">
              <button
                class="pagination_btn"
                @click="changePage(currentPage - 1)"
                :disabled="currentPage <= 1"
              >
                ← Назад
              </button>
              <button
                class="pagination_btn"
                @click="changePage(currentPage + 1)"
                :disabled="currentPage >= totalPages"
              >
                Вперёд →
              </button>
            </div>
          </div>
        </template>
      </div>
    </div>
  </main>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useTasksStore } from '@/stores/tasks_store.ts'
import {
  formatDateShort as formatDate,
  parseDeadline,
  isExpired,
  statusChip,
  statusLabel,
} from '@/utils/tasks.ts'

defineOptions({ name: 'TasksPage' })

const router = useRouter()
const tasksStore = useTasksStore()

// an available task past its deadline was never acted on and can no longer be —
// it's effectively gone, so it's filtered out here rather than left to show as actionable
const myTasks = computed(() =>
  tasksStore.myTasks.filter((t) => t.status !== 'available' || !isExpired(t.deadline)),
)

const searchQuery = ref('')
const deadlineBefore = ref('')
const deadlineAfter = ref('')
const statusFilter = ref('')
const currentPage = ref(1)
const PAGE_SIZE = 10

// <input type="date"> gives a bare "YYYY-MM-DD" string, which `new Date()` parses as
// UTC midnight rather than local midnight — a day boundary computed that way silently
// drifts by the local UTC offset. Parsing the numbers by hand and building the Date from
// local components keeps "until/from this day" meaning the full Vladivostok-local day.
function parseDateBoundary(dateStr: string, endOfDay: boolean): Date {
  const [year, month, day] = dateStr.split('-').map(Number)
  return endOfDay
    ? new Date(year!, month! - 1, day!, 23, 59, 59, 999)
    : new Date(year!, month! - 1, day!, 0, 0, 0, 0)
}

const filteredTasks = computed(() =>
  myTasks.value.filter((t) => {
    if (searchQuery.value && !t.title.toLowerCase().includes(searchQuery.value.toLowerCase()))
      return false
    if (statusFilter.value && t.status !== statusFilter.value) return false
    if (
      deadlineBefore.value &&
      parseDeadline(t.deadline) > parseDateBoundary(deadlineBefore.value, true)
    )
      return false
    if (
      deadlineAfter.value &&
      parseDeadline(t.deadline) < parseDateBoundary(deadlineAfter.value, false)
    )
      return false
    return true
  }),
)

const paginatedTasks = computed(() => {
  const start = (currentPage.value - 1) * PAGE_SIZE
  return filteredTasks.value.slice(start, start + PAGE_SIZE)
})

const totalPages = computed(() => Math.max(1, Math.ceil(filteredTasks.value.length / PAGE_SIZE)))

const activeTasks = computed(() =>
  myTasks.value.filter((t) => t.status === 'available').slice(0, 3),
)
const pendingTasks = computed(() => myTasks.value.filter((t) => t.status === 'pending'))
const rejectedTasks = computed(() => myTasks.value.filter((t) => t.status === 'rejected'))

const recentCompleted = computed(() =>
  myTasks.value.filter((t) => t.status === 'accepted').slice(0, 3),
)

const totalCount = computed(
  () =>
    myTasks.value.filter((t) => t.status === 'rejected').length +
    myTasks.value.filter((t) => t.status === 'accepted').length,
)
const completedCount = computed(() => myTasks.value.filter((t) => t.status === 'accepted').length)
const progress = computed(() =>
  totalCount.value ? Math.round((completedCount.value / totalCount.value) * 100) : 0,
)

const animatedProgress = ref(0)
const PROGRESS_FILL_DURATION = 600

onMounted(async () => {
  await tasksStore.fetchMyTasks()

  const target = progress.value
  const start = performance.now()

  function tick(now: number): void {
    const t = Math.min((now - start) / PROGRESS_FILL_DURATION, 1)
    animatedProgress.value = Math.round(target * t)
    if (t < 1) requestAnimationFrame(tick)
  }

  requestAnimationFrame(tick)
})

function applyFilters(): void {
  currentPage.value = 1
}

function clearFilters(): void {
  searchQuery.value = ''
  deadlineBefore.value = ''
  deadlineAfter.value = ''
  statusFilter.value = ''
  currentPage.value = 1
}

function changePage(page: number): void {
  if (page < 1 || page > totalPages.value) return
  currentPage.value = page
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

/* hero */

.page_hero {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 28px 32px;
  background-color: white;
  border-radius: 16px;
  margin-top: 32px;
  box-shadow: 0px 0px 15px 0px rgba(0, 0, 0, 0.1);
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

/* main grid */

.tasks_grid {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.grid_top {
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: 24px;
}

/* Grid's default align-items: stretch makes the left card match the height
   of the right column (pending + rejected stacked), so it grows down to the
   bottom of "Отклонённые" instead of leaving empty space below itself. */
.grid_bottom {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.grades_card {
  display: flex;
  flex-direction: column;
}

.grades_footer_btn {
  margin-top: auto;
}

.grid_bottom_right {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* cards */

.card {
  background-color: white;
  border-radius: 16px;
  box-shadow: 0px 0px 15px 0px rgba(0, 0, 0, 0.1);
  padding: 24px;
}

.card_progress {
  display: flex;
  flex-direction: column;
  background-color: white;
  border-radius: 16px;
  box-shadow: 0px 0px 15px 0px rgba(0, 0, 0, 0.1);
  padding: 24px;
}

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

/* active assignments */

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
  padding: 14px 16px;
  border-radius: 12px;
  background-color: rgb(244, 243, 250);
  cursor: pointer;
  transition:
    0.2s background-color,
    0.2s transform;
}

.assignment_item:hover {
  background-color: rgb(235, 230, 245);
  transform: translateX(6px);
}

.assignment_title {
  font-family: Nagel;
  font-size: 15px;
  color: rgb(65, 65, 65);
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

/* view all button */

.view_all_btn {
  appearance: none;
  width: 100%;
  margin-top: 16px;
  border: thin solid rgb(210, 208, 220);
  border-radius: 10px;
  padding: 10px;
  font-family: Nagel;
  font-size: 14px;
  cursor: pointer;
  background-color: white;
  color: rgb(65, 65, 65);
  transition: 0.2s background-color;
}

.view_all_btn:hover {
  background-color: rgb(244, 243, 250);
}

/* grades */

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
  border-radius: 12px;
  background-color: rgb(160, 125, 180);
  font-family: Nagel;
  font-size: 16px;
  color: white;
  flex-shrink: 0;
}

/* progress */

.progress_circle_wrap {
  display: flex;
  justify-content: center;
  margin: 12px 0 16px;
}

.progress_circle {
  width: 120px;
  height: 120px;
  border-radius: 999px;
  display: flex;
  align-items: center;
  justify-content: center;
  background:
    radial-gradient(white 56%, transparent 58%),
    conic-gradient(rgb(160, 125, 180) 0% calc(var(--progress) * 1%), rgb(230, 228, 240) 0%);
}

.progress_inner {
  font-family: Nagel;
  font-size: 24px;
  color: rgb(65, 65, 65);
}

.progress_info {
  font-family: Nagel;
  font-size: 13px;
  color: rgb(150, 150, 150);
  text-align: center;
  margin: 0 0 14px;
}

.progress_bar {
  height: 8px;
  border-radius: 999px;
  background-color: rgb(230, 228, 240);
  overflow: hidden;
}

.progress_fill {
  height: 100%;
  border-radius: inherit;
  background-color: rgb(160, 125, 180);
  transition: 0.4s width;
}

/* pending review */

.pending_list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.pending_item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  padding: 12px 14px;
  border-radius: 12px;
  background-color: rgba(202, 138, 4, 0.08);
}

.rejected_item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  padding: 12px 14px;
  border-radius: 12px;
  background-color: rgba(204, 63, 75, 0.08);
  cursor: pointer;
  transition: 0.2s background-color;
}

.rejected_item:hover {
  background-color: rgba(204, 63, 75, 0.14);
}

.pending_title {
  font-family: Nagel;
  font-size: 14px;
  color: rgb(65, 65, 65);
}

/* states */

.empty_state {
  padding: 32px 16px;
  text-align: center;
  font-family: Nagel;
  color: rgb(150, 150, 150);
  font-size: 14px;
}

.ok_state {
  padding: 14px 16px;
  border-radius: 12px;
  background-color: rgba(22, 163, 74, 0.08);
  font-family: Nagel;
  font-size: 14px;
  color: rgb(22, 163, 74);
  text-align: center;
}

/* status chips */

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

/* filters */

.filters_card {
  padding: 20px 24px;
}

.filters_row {
  display: flex;
  flex-wrap: wrap;
  align-items: flex-end;
  gap: 12px;
}

.filter_field {
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-width: 140px;
  flex: 1;
}

.filter_label {
  font-family: Nagel;
  font-size: 13px;
  color: rgb(150, 150, 150);
}

.filter_input {
  appearance: none;
  border: thin solid rgb(210, 208, 220);
  border-radius: 10px;
  padding: 8px 12px;
  font-family: Nagel;
  font-size: 14px;
  color: rgb(65, 65, 65);
  background-color: white;
  outline: none;
  transition: 0.2s border-color;
}

.filter_input:focus {
  border-color: rgb(160, 125, 180);
}

.filter_actions {
  display: flex;
  gap: 8px;
  align-items: flex-end;
  padding-bottom: 1px;
}

.filter_btn {
  appearance: none;
  border: thin solid rgb(210, 208, 220);
  border-radius: 10px;
  padding: 8px 16px;
  font-family: Nagel;
  font-size: 14px;
  cursor: pointer;
  background-color: white;
  color: rgb(65, 65, 65);
  white-space: nowrap;
  transition: 0.2s background-color;
}

.filter_btn:hover {
  background-color: rgb(244, 243, 250);
}

.filter_btn_primary {
  background-color: rgb(160, 125, 180);
  border-color: rgb(160, 125, 180);
  color: white;
}

.filter_btn_primary:hover {
  background-color: rgb(140, 105, 160);
}

/* table */

.table_card {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.table_wrap {
  overflow-x: auto;
}

.tasks_table {
  width: 100%;
  border-collapse: collapse;
  font-family: Nagel;
  font-size: 14px;
  color: rgb(65, 65, 65);
}

.tasks_table th {
  text-align: left;
  padding: 10px 14px;
  border-bottom: thin solid rgb(230, 228, 240);
  color: rgb(150, 150, 150);
  font-size: 13px;
  white-space: nowrap;
}

.tasks_table td {
  padding: 12px 14px;
  border-bottom: thin solid rgb(244, 243, 250);
}

.task_row {
  cursor: pointer;
}

.tasks_table tbody tr:hover td {
  background-color: rgb(250, 249, 252);
}

.tasks_table tbody tr:last-child td {
  border-bottom: none;
}

/* pagination */

.pagination_bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
}

.pagination_info {
  font-family: Nagel;
  font-size: 13px;
  color: rgb(150, 150, 150);
}

.pagination_btns {
  display: flex;
  gap: 8px;
}

.pagination_btn {
  appearance: none;
  border: thin solid rgb(210, 208, 220);
  border-radius: 10px;
  padding: 6px 14px;
  font-family: Nagel;
  font-size: 14px;
  cursor: pointer;
  background-color: white;
  color: rgb(65, 65, 65);
  transition: 0.2s background-color;
}

.pagination_btn:hover:not(:disabled) {
  background-color: rgb(160, 125, 180);
  border-color: rgb(160, 125, 180);
  color: white;
}

.pagination_btn:disabled {
  opacity: 0.4;
  cursor: default;
}

/* responsive */

@media screen and (max-width: 1050px) {
  main {
    padding-inline: 16px;
  }

  .main_contents {
    width: 100%;
  }

  .grid_top {
    grid-template-columns: 1fr;
  }

  .grid_bottom {
    grid-template-columns: 1fr;
  }
}

@media screen and (max-width: 540px) {
  .main_contents {
    padding-top: 70px;
  }

  .filters_row {
    flex-direction: column;
  }

  .filter_field {
    width: 100%;
  }

  .pagination_bar {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
