<template>
  <v-app class="main-class">

    <v-app-bar app color="blue-grey darken-1" dark dense clipped-left flat>
      <div class="d-flex align-center">
        <v-img
          alt="Vuetify Logo"
          class="shrink mr-2"
          contain
          src="./assets/logos/hierarchical-structure.png"
          transition="scale-transition"
          width="40"
        />
        <span class="text-sm-h6 text-subtitle-2" style="margin-left: 4px">Multi Label Learning Platform</span>
      </div>

      <v-spacer></v-spacer>

      <v-btn
        href="https://github.com/vuetifyjs/vuetify/releases/latest"
        target="_blank"
        text
      >
        <span class="mr-2">Latest Release</span>
        <v-icon>mdi-open-in-new</v-icon>
      </v-btn>
    </v-app-bar>

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
      { title: 'Label Space', icon: 'mdi-image', link: "/labelspace" },
      { title: '数据列表', icon: 'mdi-file-table', link: "/viewdata" },
      { title: 'Statistic', icon: 'mdi-poll-box', link: "/stat" },
      { title: 'Debug', icon: 'mdi-help-box', link: "/about" },
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