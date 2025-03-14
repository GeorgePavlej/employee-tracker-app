<template>
  <div>
    <h2>Zobraziť záznamy</h2>
    <v-row dense>
      <v-col cols="12" md="3">
        <v-text-field
            v-model="logsFilter.name"
            label="Meno zamestnanca (obsahuje)"
            outlined
        ></v-text-field>
      </v-col>
      <v-col cols="12" md="3">
        <v-text-field
            v-model="logsFilter.dateFrom"
            type="date"
            label="Dátum od"
            outlined
        ></v-text-field>
      </v-col>
      <v-col cols="12" md="3">
        <v-text-field
            v-model="logsFilter.dateTo"
            type="date"
            label="Dátum do"
            outlined
        ></v-text-field>
      </v-col>
      <v-col cols="12" md="3" class="text-right">
        <v-btn color="primary" @click="viewLogs">Filtrovať záznamy</v-btn>
      </v-col>
    </v-row>

    <v-data-table :items="logs" class="mt-4" dense>
      <template v-slot:headers>
        <tr>
          <th class="text-left">Meno zamestnanca</th>
          <th class="text-left">Dátum</th>
          <th class="text-left">Príchod</th>
          <th class="text-left">Odchod</th>
          <th class="text-left">Začiatok obeda</th>
          <th class="text-left">Koniec obeda</th>
        </tr>
      </template>
      <template v-slot:body="{ items }">
        <tr v-if="items.length === 0">
          <td colspan="6" class="text-center">
            Pre dané filtre neboli nájdené žiadne záznamy.
          </td>
        </tr>
        <tr v-for="(log, index) in items" :key="index">
          <td>{{ log.employee_name }}</td>
          <td>{{ log.date }}</td>
          <td>{{ log.clock_in_time || 'N/A' }}</td>
          <td>{{ log.clock_out_time || 'N/A' }}</td>
          <td>{{ log.lunch_start_time || 'N/A' }}</td>
          <td>{{ log.lunch_end_time || 'N/A' }}</td>
        </tr>
      </template>
    </v-data-table>
  </div>
</template>

<script>
const baseURL = process.env.VUE_APP_API_URL;

export default {
  name: 'LogsView',
  data() {
    return {
      logsFilter: {
        name: '',
        dateFrom: '',
        dateTo: '',
      },
      logs: []
    };
  },
  created() {
    this.viewLogs();
  },
  methods: {
    viewLogs() {
      const {name, dateFrom, dateTo} = this.logsFilter;
      let url = `${baseURL}/logs/?`;
      const params = [];
      if (name) {
        params.push(`employee_name=${encodeURIComponent(name)}`);
      }
      if (dateFrom) {
        params.push(`date_from=${dateFrom}`);
      }
      if (dateTo) {
        params.push(`date_to=${dateTo}`);
      }
      url += params.join('&');

      fetch(url)
          .then(res => res.json())
          .then(data => {
            this.logs = data;
          })
          .catch(error => {
            console.error('Error:', error);
            alert('Nastala chyba pri načítaní záznamov.');
          });
    }
  }
};
</script> 