<template>
  <div class="md-layout-column">
  
    <md-toolbar class="md-primary">
      <md-button class="md-icon-button" @click="showNavigation = true">
        <md-icon>menu</md-icon>
      </md-button>
      <span class="md-title">Управление остатками</span>
    </md-toolbar>

    <md-drawer :md-active.sync="showNavigation">
      <md-toolbar class="md-transparent" md-elevation="0">
        <span class="md-title">Меню</span>
      </md-toolbar>
    </md-drawer>

  </div>
</template>

<script>
    export default {
        name: 'Sidenav',
        data: () => ({
            showNavigation: false
        }),
        components: {
        }
    }
</script>

<style lang="scss" scoped>
    body {
        height: 100%;
        width: 100%;
    }

  .md-drawer {
    width: 230px;
    max-width: calc(100vw - 125px);
  }

  .md-content {
    padding: 16px;
  }

  .md-card {
      padding: 16px;
  }

  .app {
      height: 100%;
  }
</style>