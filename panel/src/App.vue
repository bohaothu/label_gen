<template>
  <v-app>

    <v-app-bar app color="primary" dark dense clipped-left flat>
      <div class="d-flex align-center">
        <v-img
          alt="Vuetify Logo"
          class="shrink mr-2"
          contain
          src="https://cdn.vuetifyjs.com/images/logos/vuetify-logo-dark.png"
          transition="scale-transition"
          width="40"
        />

        <v-img
          alt="Vuetify Name"
          class="shrink mt-1 hidden-sm-and-down"
          contain
          min-width="100"
          src="https://cdn.vuetifyjs.com/images/logos/vuetify-name-dark.png"
          width="100"
        />
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

    <v-navigation-drawer v-model="toggle" clipped dark app>
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
      <router-view></router-view>
    </v-main>
  </v-app>
</template>

<script>

export default {
  name: 'App',

  data: () => ({
    nav: null,
    nav_items: [
      { title: '导入数据', icon: 'mdi-view-dashboard', link: "/" },
      { title: '数据列表', icon: 'mdi-file-table', link: "/viewdata" },
      { title: '统计资料', icon: 'mdi-poll-box', link: "/stat" },
      { title: 'Label 云', icon: 'mdi-image', link: "/wordcloud" },
      { title: 'Debug', icon: 'mdi-help-box', link: "/about" },
    ]
  }),
};
</script>
