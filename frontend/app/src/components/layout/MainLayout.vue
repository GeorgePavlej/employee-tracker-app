<template>
  <v-app>
    <!-- App Bar -->
    <v-app-bar app color="primary" dark>
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title>Správca zamestnancov</v-toolbar-title>
      <v-spacer></v-spacer>
      <div class="d-none d-md-flex">
        <v-btn
            v-for="item in menuItems"
            :key="item.id"
            text
            :class="{'font-weight-bold underline': isRouteActive(item.route)}"
            :to="{ name: item.route }"
        >
          {{ item.title }}
        </v-btn>
        <v-btn
            text
            color="black"
            class="ml-4"
            @click="logout"
        >
          <v-icon left>mdi-logout</v-icon>
          Odhlásiť sa
        </v-btn>
      </div>
      <v-btn
          v-if="$vuetify.display.mdAndDown"
          icon
          color="error"
          @click="logout"
          class="ml-2"
      >
        <v-icon>mdi-logout</v-icon>
      </v-btn>
    </v-app-bar>

    <!-- Navigation Drawer -->
    <v-navigation-drawer
        v-model="drawer"
        app
        temporary
        color="primary"
        dark
    >
      <v-list dense>
        <v-list-item
            v-for="item in menuItems"
            :key="item.id"
            :to="{ name: item.route }"
            @click="drawer = false"
        >
          <v-list-item-content>
            <div class="d-flex align-center">
              <span :class="{'font-weight-bold underline': isRouteActive(item.route)}">
                {{ item.title }}
              </span>
              <v-icon class="ml-2">{{ item.icon }}</v-icon>
            </div>
          </v-list-item-content>
        </v-list-item>
        
        <v-divider class="my-2"></v-divider>
        
        <v-list-item @click="logout">
          <v-list-item-content>
            <div class="d-flex align-center">
              <span class="error--text">Odhlásiť sa</span>
              <v-icon class="ml-2 error--text">mdi-logout</v-icon>
            </div>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <!-- Main Content -->
    <v-main>
      <v-container fluid class="mt-4">
        <!-- Router View for Child Routes -->
        <router-view :employees="employees" @employee-updated="loadEmployees"></router-view>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import { clearTokens } from '../../utils/auth';

const baseURL = process.env.VUE_APP_API_URL;

export default {
  name: 'MainLayout',
  data() {
    return {
      drawer: false,
      menuItems: [
        {id: 'clockInOut', title: 'Príchod/Odchod', icon: 'mdi-clock-outline', route: 'clockInOut'},
        {id: 'logs', title: 'Záznamy', icon: 'mdi-file-document-outline', route: 'logs'},
        {id: 'shifts', title: 'Smeny', icon: 'mdi-calendar-clock', route: 'shifts'},
        {id: 'reports', title: 'Správy', icon: 'mdi-chart-bar', route: 'reports'},
        {id: 'leaveManagement', title: 'Správa dovoleniek', icon: 'mdi-beach', route: 'leaveManagement'},
        {id: 'employeeManagement', title: 'Správa zamestnancov', icon: 'mdi-account-group', route: 'employeeManagement'},
      ],
      employees: []
    };
  },
  created() {
    this.loadEmployees();
  },
  methods: {
    isRouteActive(routeName) {
      return this.$route.name === routeName;
    },
    loadEmployees() {
      fetch(`${baseURL}/employees/`)
          .then(res => res.json())
          .then(data => {
            this.employees = data;
          })
          .catch(error => console.error('Error fetching employees:', error));
    },
    logout() {
      clearTokens();
      this.$router.push({ name: 'login' });
    }
  }
};
</script>

<style scoped>
.underline {
  text-decoration: underline;
}

.font-weight-bold {
  font-weight: 600 !important;
}

.mb-3 {
  margin-bottom: 16px;
}

.mt-4 {
  margin-top: 24px;
}
</style> 