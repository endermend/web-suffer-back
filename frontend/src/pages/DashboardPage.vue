<template>
  <main>
    <div class="main_contents page_enter">
      <section class="banners">
        <swiper
          :pagination="true"
          :modules="modules"
          :autoplay="{ delay: 5000, disableOnInteraction: false }"
          class="swiper_carousel"
        >
          <swiper-slide v-for="slide in slides" :key="slide.id">
            <img :src="slide.image" class="swiper_image" />
            <div class="slide_caption">
              <span class="slide_caption_title">{{ slide.title }}</span>
            </div>
          </swiper-slide>
        </swiper>
      </section>

      <section class="leaderboard_section">
        <div class="leaderboard_card">
          <h2 class="leaderboard_title">Таблица лидеров</h2>
          <div class="leaderboard_table">
            <div class="leaderboard_header">
              <span class="col_rank">#</span>
              <span class="col_name_header">Почта</span>
              <span class="col_points">Очки</span>
            </div>
            <div v-for="(entry, index) in leaderboard" :key="entry.label" class="leaderboard_row">
              <span class="col_rank">
                <MedalIcon v-if="index === 0" class="rank_gold" />
                <MedalIcon v-else-if="index === 1" class="rank_silver" />
                <MedalIcon v-else-if="index === 2" class="rank_bronze" />
                <span v-else class="rank_plain">{{ index + 1 }}</span>
              </span>
              <span class="col_name">{{ entry.label }}</span>
              <span class="col_points">{{ entry.exp }}</span>
            </div>
          </div>
        </div>
      </section>
    </div>
  </main>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Swiper, SwiperSlide } from 'swiper/vue'
import 'swiper/css'
import 'swiper/css/pagination'
import { Pagination, Autoplay } from 'swiper/modules'
import beachImg from '@/assets/images/beach.jpg'
import starfishImg from '@/assets/images/starfish.jpg'
import grissomImg from '@/assets/images/grissom.png'
import surpriseImg from '@/assets/images/surprise.gif'
import hourswith777 from '@/assets/images/2hours.gif'
import taskService from '@/services/api/task_service.ts'
import MedalIcon from '@/assets/icons/medal.svg'

defineOptions({ name: 'DashboardPage' })

const leaderboard = ref<{ label: string; exp: number }[]>([])

onMounted(async () => {
  const topUsers = await taskService.getTopUsers(5)
  leaderboard.value = topUsers.map((u) => ({ label: u.user_email, exp: u.exp }))
})

const modules = [Pagination, Autoplay]

const slides = ref([
  {
    id: 1,
    image: beachImg,
    title:
      'Я вы были в Майами? Майами Майами Я когда был в Майами Майами Майами Майами вот я реально когда был в Майами Майами Майами это Майами Бич отдельно Майами Посмотрите пожалуйста моё видео из Майами Бич Майами это реальный Майами Майами',
  },
  {
    id: 2,
    image: starfishImg,
    title: 'Вы готовы дети? Да капитан! Я не слышу! Так точно капитан!',
  },
  {
    id: 3,
    image: grissomImg,
    title: 'Последние новости: Гриссом приземлился на поверхность экзопланеты "Альфа Изатои IV"',
  },
  {
    id: 4,
    image: surpriseImg,
    title: 'Ой не то видео простите',
  },
  {
    id: 5,
    image: hourswith777,
    title: '2 HOURS WITHOUT 777 AND THE WEBSITE IS NOT FINISHED',
  },
])
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
  width: 1000px;
  display: flex;
  flex-direction: column;
}

/* swiper */

.banners {
  height: 600px;
  margin-block: 30px;
  box-shadow: 0px 0px 15px 0px rgba(0, 0, 0, 0.1);
  border: none;
  border-radius: 16px;
  overflow: hidden;
}

.swiper_carousel {
  height: 100%;
  width: 100%;
  border: none;
  border-radius: 16px;
  z-index: 0;
}

:deep(.swiper-slide) {
  position: relative;
}

:deep(.swiper-pagination-bullet) {
  background: rgb(160, 125, 180);
  opacity: 0.6;
}

:deep(.swiper-pagination-bullet-active) {
  opacity: 1;
}

.swiper_image {
  object-fit: cover;
  width: 100%;
  height: 100%;
}

.slide_caption {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 28px 28px;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.55) 0%, transparent 100%);
  z-index: 1;
}

.slide_caption_title {
  font-family: Nagel;
  font-size: 22px;
  color: white;
}

/* leaderboard */

.leaderboard_section {
  margin-bottom: 40px;
}

.leaderboard_card {
  background: white;
  border: none;
  border-radius: 16px;
  box-shadow: 0px 0px 15px 0px rgba(0, 0, 0, 0.1);
  padding: 24px;
}

.leaderboard_title {
  font-family: Nagel;
  font-size: 1.4rem;
  color: rgb(65, 65, 65);
  margin-bottom: 20px;
}

.leaderboard_table {
  display: flex;
  flex-direction: column;
}

.leaderboard_header {
  display: grid;
  grid-template-columns: 64px 1fr 50px;
  padding: 10px 16px;
  background: rgb(244, 243, 250);
  border: none;
  border-radius: 8px;
  margin-bottom: 4px;
  font-family: Nagel;
  font-size: 13px;
  color: rgb(150, 150, 150);
}

.leaderboard_row {
  display: grid;
  grid-template-columns: 64px 1fr 50px;
  padding: 0px;
  border-bottom: 1px solid rgb(230, 228, 240);
  font-family: Nagel;
  color: rgb(65, 65, 65);
  transition: background-color 0.15s;
  align-items: center;
}

.leaderboard_row:last-child {
  border-bottom: none;
}

.leaderboard_row:hover {
  background-color: rgb(248, 247, 253);
}

.col_rank {
  display: flex;
  align-items: center;
  align-content: center;
}

.col_name_header {
  word-break: break-all;
  min-width: 0px;
  padding: 16px;
  font-size: 16px;
}

.col_name {
  word-break: break-all;
  min-width: 0px;
  padding: 16px;
  font-size: 16px;
  cursor: pointer;
  transition:
    transform 0.4s ease,
    background-color 0.15s;
}

.col_name:hover {
  transform: translateX(8px);
}

.col_points {
  font-size: 16px;
  padding: 16px;
  font-weight: bold;
  color: rgb(160, 125, 180);
  text-align: right;
}

.rank_gold {
  padding: 16px;
  color: #e0a820;
  height: 100%;
}
.rank_silver {
  padding: 16px;
  color: #9ea6b4;
  height: 100%;
}
.rank_bronze {
  padding: 16px;
  color: #b07040;
  height: 100%;
}

.rank_plain {
  padding-inline: 30px;
  font-size: 14px;
  color: rgb(150, 150, 150);
}

/* media screen */

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

  .banners {
    height: 500px;
  }

  .slide_caption_title {
    font-size: 4vw;
  }
}
</style>
