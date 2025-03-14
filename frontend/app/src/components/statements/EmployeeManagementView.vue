<template>
  <div>
    <h2>Správa zamestnancov</h2>

    <v-form ref="employeeForm">
      <v-row dense>
        <v-col cols="12" md="4">
          <v-text-field
              v-model="employeeFormData.name"
              label="Meno zamestnanca"
              outlined
          ></v-text-field>
        </v-col>
        <v-col cols="12" md="4" class="text-right">
          <v-btn
              color="primary"
              v-if="!editMode"
              @click="createEmployee"
          >
            Vytvoriť zamestnanca
          </v-btn>

          <v-btn
              color="success"
              v-if="editMode"
              @click="updateEmployee"
          >
            Aktualizovať zamestnanca
          </v-btn>

          <v-btn
              color="secondary"
              v-if="editMode"
              @click="cancelEdit"
          >
            Zrušiť
          </v-btn>
        </v-col>
      </v-row>
    </v-form>

    <hr class="my-4"/>

    <v-data-table :items="employees" dense>
      <template v-slot:headers>
        <tr>
          <th>ID zamestnanca</th>
          <th>Meno</th>
          <th class="text-right">Akcie</th>
        </tr>
      </template>
      <template v-slot:body="{ items }">
        <tr v-if="items.length === 0">
          <td colspan="3" class="text-center">
            Žiadni zamestnanci neboli nájdení.
          </td>
        </tr>
        <tr v-for="(emp, index) in items" :key="index">
          <td>{{ emp.employee_id }}</td>
          <td>{{ emp.name }}</td>
          <td class="text-right">
            <v-btn
                small
                color="warning"
                @click="editEmployee(emp)"
            >
              Upraviť
            </v-btn>
            <v-btn
                small
                color="error"
                @click="deleteEmployee(emp.employee_id)"
            >
              Vymazať
            </v-btn>
          </td>
        </tr>
      </template>
    </v-data-table>
  </div>
</template>

<script>
const baseURL = process.env.VUE_APP_API_URL;

export default {
  name: 'EmployeeManagementView',
  props: {
    employees: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      employeeFormData: {
        employee_id: null,
        name: '',
      },
      editMode: false
    };
  },
  methods: {
    createEmployee() {
      if (!this.employeeFormData.name) {
        alert('Prosím, zadajte meno.');
        return;
      }
      fetch(`${baseURL}/employees/`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({name: this.employeeFormData.name}),
      })
          .then(res => {
            if (!res.ok) {
              return res.json().then(data => {
                throw new Error(data.detail || 'Chyba pri vytváraní zamestnanca.');
              });
            }
            return res.json();
          })
          .then(newEmployee => {
            alert('Zamestnanec bol úspešne vytvorený.');
            this.employeeFormData.name = '';
            this.$emit('employee-updated');
          })
          .catch(error => {
            console.error(error);
            alert(error.message);
          });
    },
    deleteEmployee(employeeId) {
      if (!confirm('Ste si istí, že chcete vymazať tohto zamestnanca?')) return;

      fetch(`${baseURL}/employees/${employeeId}/`, {
        method: 'DELETE',
      })
          .then(async res => {
            if (!res.ok) {
              let err = 'Chyba pri odstraňovaní zamestnanca.';
              try {
                const data = await res.json();
                err = data.detail || err;
              } catch {
              }
              throw new Error(err);
            }
            return res.json();
          })
          .then(data => {
            alert(data.message || 'Zamestnanec bol úspešne odstránený.');
            this.$emit('employee-updated');
          })
          .catch(error => {
            console.error(error);
            alert(error.message);
          });
    },
    editEmployee(emp) {
      this.editMode = true;
      this.employeeFormData.employee_id = emp.employee_id;
      this.employeeFormData.name = emp.name;
    },
    updateEmployee() {
      const {employee_id, name} = this.employeeFormData;
      if (!employee_id || !name) {
        alert('Neplatné údaje.');
        return;
      }
      fetch(`${baseURL}/employees/${employee_id}/`, {
        method: 'PUT',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({name}),
      })
          .then(res => {
            if (!res.ok) {
              return res.json().then(data => {
                throw new Error(data.detail || 'Chyba pri aktualizácii zamestnanca.');
              });
            }
            return res.json();
          })
          .then(updatedEmployee => {
            alert('Zamestnanec bol úspešne aktualizovaný.');
            this.cancelEdit();
            this.$emit('employee-updated');
          })
          .catch(error => {
            console.error(error);
            alert(error.message);
          });
    },
    cancelEdit() {
      this.editMode = false;
      this.employeeFormData.employee_id = null;
      this.employeeFormData.name = '';
    }
  }
};
</script> 