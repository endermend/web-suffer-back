<template>
  <main>
    <div class="main_contents">
      <div class="page_hero">
        <h1 class="page_title">Управление заданиями</h1>
        <p class="page_subtitle">Создание заданий и проверка ответов участников</p>
      </div>

      <div class="card">
        <span class="card_title">Создать задание</span>
      </div>

      <div class="card">
        <span class="card_title">Проверка выполненных заданий</span>
      </div>
    </div>
  </main>
</template>

<script setup lang="ts">
defineOptions({ name: 'ManageTasksPage' })
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
  box-shadow: 0px 0px 15px 0px rgb(211, 211, 211);
  padding: 24px;
}

.card_title {
  font-family: Nagel;
  font-size: 18px;
  color: rgb(65, 65, 65);
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
}
</style>
