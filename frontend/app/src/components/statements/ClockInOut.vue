<template>
  <div>
    <h2>Príchod/Odchod</h2>
    <v-select
        v-model="selectedEmployeeClock"
        :items="employees"
        item-title="name"
        item-value="employee_id"
        label="Vyberte zamestnanca"
        outlined
    ></v-select>

    <div class="mt-4">
      <v-btn
          color="primary"
          class="mr-2"
          @click="clockIn"
          :disabled="!selectedEmployeeClock"
      >
        Príchod
      </v-btn>
      <v-btn
          color="secondary"
          class="mr-2"
          @click="clockOut"
          :disabled="!selectedEmployeeClock"
      >
        Odchod
      </v-btn>
      <v-btn
          color="warning"
          class="mr-2"
          @click="startLunch"
          :disabled="!selectedEmployeeClock"
      >
        Začať obed
      </v-btn>
      <v-btn
          color="success"
          @click="endLunch"
          :disabled="!selectedEmployeeClock"
      >
        Ukončiť obed
      </v-btn>
    </div>
  </div>
</template>

<script>
const baseURL = process.env.VUE_APP_API_URL;

export default {
  name: 'ClockInOut',
  props: {
    employees: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      selectedEmployeeClock: null
    };
  },
  methods: {
    clockIn() {
      if (!this.selectedEmployeeClock) return;
      fetch(`${baseURL}/clock_in/?employee_id=${this.selectedEmployeeClock}`, {
        method: 'POST',
      })
          .then(res => res.json())
          .then(data => {
            alert(data.message || data.detail);
          });
    },
    clockOut() {
      if (!this.selectedEmployeeClock) return;
      fetch(`${baseURL}/clock_out/?employee_id=${this.selectedEmployeeClock}`, {
        method: 'POST',
      })
          .then(res => res.json())
          .then(data => {
            alert(data.message || data.detail);
          })
          .catch(error => {
            console.error('Error:', error);
            alert('Nastala chyba pri odchode z práce.');
          });
    },
    startLunch() {
      if (!this.selectedEmployeeClock) return;
      fetch(`${baseURL}/start_lunch/?employee_id=${this.selectedEmployeeClock}`, {
        method: 'POST',
      })
          .then(res => res.json())
          .then(data => {
            alert(data.message || data.detail);
          })
          .catch(error => {
            console.error('Error:', error);
            alert('Nastala chyba pri začiatku obeda.');
          });
    },
    endLunch() {
      if (!this.selectedEmployeeClock) return;
      fetch(`${baseURL}/end_lunch/?employee_id=${this.selectedEmployeeClock}`, {
        method: 'POST',
      })
          .then(res => res.json())
          .then(data => {
            alert(data.message || data.detail);
          })
          .catch(error => {
            console.error('Error:', error);
            alert('Nastala chyba pri ukončení obeda.');
          });
    }
  }
};
</script> 