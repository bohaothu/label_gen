<template>
  <v-app class="main-class">

    <v-navigation-drawer color="light-bule darken-3" v-model="toggle" expand-on-hover clipped dark app>
      <v-list nav>
        <v-list-item v-for="item in nav_items" :key="item.title" :to="item.link">
          <v-list-item-icon><v-icon>{{ item.icon }}</v-icon></v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title> {{ item.title }} </v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-main>
      <router-view class="pa-2"></router-view>
    </v-main>
  </v-app>
</template>

<script>

export default {
  name: 'App',

  data: () => ({
    nav: null,
    nav_items: [
      { title: 'Import Data', icon: 'mdi-view-dashboard', link: "/" },
      { title: 'Visualization', icon: 'mdi-image', link: "/labelspace" },
      { title: 'Heatmap', icon: 'mdi-chart-bar', link: "/groupview" },
    ]
  }),
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

.main-class {
  font-family: Inter, Helvetica Neue, Roboto, Arial, Helvetica, Microsoft YaHei, sans-serif;
}
</style>