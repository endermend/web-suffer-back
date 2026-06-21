<template>
  <footer>
    <div class="footer_contents">
      <div>
        Наши почты:
        <span> artemonisuk03@gmail.com </span>
        <span> endermend05@gmail.com </span>
      </div>
      <div>
        Наши телеграмы:
        <span> @artmix42 </span>
        <span> @endermend </span>
      </div>
      <div class="repo_link">
        Репозиторий сайта на GitHub:
        <span> https://github.com/endermend/web-suffer-back </span>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
defineOptions({ name: 'AppFooter' })
</script>

<style scoped>
footer {
  background-color: rgb(74, 50, 83);
  width: 100%;
  box-shadow: 0px 0px 15px 0px rgb(0, 0, 0, 0.4);
  display: flex;
  justify-content: center;
}

.footer_contents {
  font-family: bahnsНа chrift;
  color: white;
  width: 1000px;
  margin-bottom: 24px;
  display: flex;
  justify-content: space-between;
}

.footer_contents div {
  margin-top: 32px;
  display: flex;
  flex-direction: column;
  margin-inline: 8px;
}

.footer_contents div span {
  width: 100%;
  text-wrap-mode: wrap;
  border-radius: 8px;
  margin-block: 8px;
  padding: 16px;
  background-color: rgb(87, 60, 97);
  border-bottom: solid rgb(168, 102, 159);
}

@media screen and (max-width: 1050px) {
  .footer_contents {
    width: 100%;
    display: grid;
    grid-template-columns: repeat(2, 1fr);
  }

  .repo_link {
    grid-column: 1 / -1;
  }
}

@media screen and (max-width: 540px) {
  .footer_contents {
    font-size: 3vw;
    margin-bottom: 120px;
  }
}
</style>
