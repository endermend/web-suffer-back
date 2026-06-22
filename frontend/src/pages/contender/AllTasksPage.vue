<template>
  <main>
    <div class="main_contents page_enter">
      <!-- hero -->
      <div class="page_hero">
        <button type="button" class="back_btn" @click="router.push('/tasks')">
          <BackArrowIcon class="back_icon" />
        </button>
        <div>
          <h1 class="page_title">Все доступные задания</h1>
          <p class="page_subtitle">Задания, которые можно взять прямо сейчас</p>
        </div>
      </div>

      <div v-if="availableTasks.length" class="masonry_grid" :style="{ '--columns': columnCount }">
        <div v-for="(column, colIndex) in columns" :key="colIndex" class="masonry_column">
          <div
            v-for="item in column"
            :key="item.id"
            class="assignment_item"
            @click="router.push(`/tasks/${item.id}`)"
          >
            <div class="assignment_title">{{ item.title }}</div>
            <div class="assignment_description">{{ item.description }}</div>
            <div class="assignment_footer">
              <div>
                <div class="deadline_label">Дедлайн</div>
                <div class="deadline_date">{{ formatDate(item.deadline) }}</div>
              </div>
              <div class="points_label">{{ item.exp }} баллов</div>
            </div>
          </div>
        </div>
      </div>
      <div v-else class="card">
        <div class="empty_state">Доступных заданий нет</div>
      </div>
    </div>
  </main>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useBreakpoints } from '@vueuse/core'
import { useTasksStore } from '@/stores/tasks_store.ts'
import { formatDateShort as formatDate, isExpired } from '@/utils/tasks.ts'
import type { UserTask } from '@/types/tasks.ts'
import BackArrowIcon from '@/assets/icons/backarrow.svg'

defineOptions({ name: 'AllTasksPage' })

const router = useRouter()
const tasksStore = useTasksStore()

onMounted(() => {
  tasksStore.fetchMyTasks()
})

const availableTasks = computed(() =>
  tasksStore.myTasks.filter((t) => t.status === 'available' && !isExpired(t.deadline)),
)

const breakpoints = useBreakpoints({ mobile: 0, tablet: 540, desktop: 1050 })
const isDesktop = breakpoints.greater('desktop')
const isTablet = breakpoints.between('tablet', 'desktop')
const columnCount = computed(() => (isDesktop.value ? 3 : isTablet.value ? 2 : 1))

// Round-robin distribution
const columns = computed(() => {
  const cols: UserTask[][] = Array.from({ length: columnCount.value }, () => [])
  availableTasks.value.forEach((task, index) => {
    cols[index % columnCount.value]!.push(task)
  })
  return cols
})
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
  align-items: center;
  gap: 16px;
  padding: 28px 32px;
  background-color: white;
  border: none;
  border-radius: 16px;
  margin-top: 32px;
  box-shadow: 0px 0px 15px 0px rgba(0, 0, 0, 0.1);
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
  border: none;
  border-radius: 16px;
  box-shadow: 0px 0px 15px 0px rgba(0, 0, 0, 0.1);
  padding: 24px;
}

.masonry_grid {
  display: grid;
  grid-template-columns: repeat(var(--columns), 1fr);
  align-items: start;
  gap: 16px;
}

.masonry_column {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.assignment_item {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 16px 18px;
  border: none;
  border-radius: 12px;
  background-color: white;
  cursor: pointer;
  transition:
    0.2s background-color,
    0.2s transform;
  box-shadow: 0px 0px 15px 0px rgb(0, 0, 0, 0.15);
}

.assignment_item:hover {
  background-color: rgb(235, 230, 245);
  transform: translateY(-4px);
}

.assignment_title {
  font-family: Nagel;
  font-size: 15px;
  color: rgb(65, 65, 65);
}

.assignment_description {
  font-family: Nagel;
  font-size: 13px;
  color: rgb(150, 150, 150);
  white-space: pre-wrap;
}

.assignment_footer {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
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
  flex-shrink: 0;
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
}
</style>
