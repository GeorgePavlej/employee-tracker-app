<template>
  <v-app>
    <v-main>

      <Statements />
    </v-main>
  </v-app>
</template>

<script>
import Statements from './views/Statements.vue';

export default {
  name: 'App',
  components: {
    Statements
  }
};
</script>

<style>
/* Global styles if needed */
</style>
