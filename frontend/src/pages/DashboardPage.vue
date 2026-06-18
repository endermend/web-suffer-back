<template>
  <main>
    <div class="main_contents">
      <section class="banners">
        <swiper :pagination="true" :modules="modules" class="swiper_carousel">
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
              <span class="col_name">Имя</span>
              <span class="col_points">Очки</span>
            </div>
            <div v-for="entry in leaderboard" :key="entry.rank" class="leaderboard_row">
              <span class="col_rank">
                <span v-if="entry.rank === 1" class="rank_badge rank_gold">1</span>
                <span v-else-if="entry.rank === 2" class="rank_badge rank_silver">2</span>
                <span v-else-if="entry.rank === 3" class="rank_badge rank_bronze">3</span>
                <span v-else class="rank_plain">{{ entry.rank }}</span>
              </span>
              <span class="col_name">{{ entry.name }}</span>
              <span class="col_points">{{ entry.points }}</span>
            </div>
          </div>
        </div>
      </section>
    </div>
  </main>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Swiper, SwiperSlide } from 'swiper/vue'
import 'swiper/css'
import 'swiper/css/pagination'
import { Pagination } from 'swiper/modules'
import beachImg from '@/assets/images/beach.jpg'
import starfishImg from '@/assets/images/starfish.jpg'

defineOptions({ name: 'DashboardPage' })

const modules = [Pagination]

interface Slide {
  id: number
  image: string
  title: string
}

interface LeaderboardEntry {
  rank: number
  name: string
  points: number
}

// TODO: replace with API call
const slides = ref<Slide[]>([
  {
    id: 1,
    image: beachImg,
    title:
      'А вы были в Майами? Майами Майами Майами Майами Майами Майами Майами Майами Майами Майами Майами а вот я был в майами',
  },
  { id: 2, image: starfishImg, title: 'Вы готовы дети? Да капитан Я не слышу Так точно капитан' },
])

// TODO: replace with API call
const leaderboard = ref<LeaderboardEntry[]>([
  { rank: 1, name: 'Денис королев', points: 1240 },
  { rank: 2, name: 'endermend1', points: 1105 },
  { rank: 3, name: 'Упростил по жести', points: 980 },
  { rank: 4, name: 'Новый чомпион', points: 500 },
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
  box-shadow: 0px 0px 15px 0px rgb(211, 211, 211);
  border-radius: 16px;
  overflow: hidden;
}

.swiper_carousel {
  height: 100%;
  width: 100%;
  border-radius: 16px;
  z-index: 0;
}

:deep(.swiper-slide) {
  position: relative;
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
  border-radius: 16px;
  box-shadow: 0px 0px 15px 0px rgb(211, 211, 211);
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
  grid-template-columns: 64px 1fr 100px;
  padding: 10px 16px;
  background: rgb(244, 243, 250);
  border-radius: 8px;
  margin-bottom: 4px;
  font-family: Nagel;
  font-size: 13px;
  color: rgb(150, 150, 150);
}

.leaderboard_row {
  display: grid;
  grid-template-columns: 64px 1fr 100px;
  padding: 14px 16px;
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
}

.col_name {
  font-size: 16px;
}

.col_points {
  font-size: 16px;
  font-weight: bold;
  color: rgb(160, 125, 180);
  text-align: right;
}

.rank_badge {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  color: white;
  font-family: Nagel;
}

.rank_gold {
  background-color: #e0a820;
}
.rank_silver {
  background-color: #9ea6b4;
}
.rank_bronze {
  background-color: #b07040;
}

.rank_plain {
  font-size: 14px;
  color: rgb(150, 150, 150);
}

/* media screen */

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

  .banners {
    height: 500px;
  }

  .slide_caption_title {
    font-size: 4vw;
  }
}
</style>
