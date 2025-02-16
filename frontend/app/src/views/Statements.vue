<template>
  <v-app>
    <!-- Mobile Navigation Drawer -->
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
            @click="selectMenu(item.id)"
        >
          <v-list-item-content>
            <div class="d-flex align-center">
              <span :class="{'font-weight-bold underline': currentSection === item.id}">
                {{ item.title }}
              </span>
              <v-icon class="ml-2">{{ item.icon }}</v-icon>
            </div>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <!-- App Bar -->
    <v-app-bar app color="primary" dark>
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title>Manažér zamestnancov</v-toolbar-title>
      <v-spacer></v-spacer>
      <div class="d-none d-md-flex">
        <v-btn
            text
            :class="{'font-weight-bold underline': currentSection === 'clockInOut'}"
            @click="showSection('clockInOut')"
        >
          Príchod/Odchod
        </v-btn>
        <v-btn
            text
            :class="{'font-weight-bold underline': currentSection === 'logs'}"
            @click="showSection('logs')"
        >
          Záznamy
        </v-btn>
        <v-btn
            text
            :class="{'font-weight-bold underline': currentSection === 'shifts'}"
            @click="showSection('shifts')"
        >
          Zmeny
        </v-btn>
        <v-btn
            text
            :class="{'font-weight-bold underline': currentSection === 'reports'}"
            @click="showSection('reports')"
        >
          Reporty
        </v-btn>
        <v-btn
            text
            :class="{'font-weight-bold underline': currentSection === 'leaveManagement'}"
            @click="showSection('leaveManagement')"
        >
          Správa dovoleniek
        </v-btn>
        <v-btn
            text
            :class="{'font-weight-bold underline': currentSection === 'employeeManagement'}"
            @click="showSection('employeeManagement')"
        >
          Správa zamestnancov
        </v-btn>
      </div>
    </v-app-bar>

    <!-- Main Content -->
    <v-main>
      <v-container fluid class="mt-4">
        <!-- CLOCK IN/OUT SECTION -->
        <div v-if="currentSection === 'clockInOut'">
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

        <!-- LOGS SECTION -->
        <div v-if="currentSection === 'logs'">
          <h2>Prehľad záznamov</h2>
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
                  Neboli nájdené žiadne záznamy pre dané filtre.
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

      </v-container>
    </v-main>
  </v-app>
</template>


<script>
const baseURL = process.env.VUE_APP_API_URL;
export default {
  name: 'Statements',
  data() {
    return {
      drawer: false,
      currentSection: 'clockInOut',
      menuItems: [
        {id: 'clockInOut', title: 'Clock In/Out', icon: 'mdi-clock-outline'},
        {id: 'logs', title: 'Logs', icon: 'mdi-file-document-outline'},
        {id: 'shifts', title: 'Shifts', icon: 'mdi-calendar-clock'},
        {id: 'reports', title: 'Reports', icon: 'mdi-chart-bar'},
        {id: 'leaveManagement', title: 'Leave Management', icon: 'mdi-beach'},
        {id: 'employeeManagement', title: 'Employee Management', icon: 'mdi-account-group'},
      ],
      employees: [],
      selectedEmployeeClock: null,
      logsFilter: {
        name: '',
        dateFrom: '',
        dateTo: ''
      },
      logs: [],
      shiftFormData: {
        employee_id: null,
        date: '',
        start_time: '',
        end_time: ''
      },
      shiftFilter: {
        employee_id: null,
        date_from: '',
        date_to: ''
      },
      shifts: [],
      reportFilter: {
        employee_id: null,
        date_from: '',
        date_to: ''
      },
      reportResult: null,
      leaveRequest: {
        employee_id: null,
        start_date: '',
        end_date: '',
        reason: '',
      },
      leaveRequests: [],
      employeeFormData: {
        employee_id: null,
        name: '',
      },
      editMode: false,
    };
  },

  created() {
    this.loadEmployees();
  },

  methods: {
    showSection(sectionId) {
      this.currentSection = sectionId;

      if (sectionId === 'shifts') {
        this.loadShifts();
      } else if (sectionId === 'logs') {
        this.viewLogs();
      } else if (sectionId === 'leaveManagement') {
        this.loadLeaveRequests();
      } else if (sectionId === 'reports') {
        this.reportResult = null;
      } else if (sectionId === 'employeeManagement') {
        this.loadEmployees();
        this.cancelEdit();
      }
    },
    selectMenu(sectionId) {
      this.showSection(sectionId);
      this.drawer = false;
    },
    formatHours(hours) {
      if (!hours) return '0.00';
      return Number(hours).toFixed(2);
    },

    // ---- EMPLOYEES ----
    loadEmployees() {
      fetch(`${baseURL}/employees/`)
          .then((res) => res.json())
          .then((data) => {
            console.log('Employees fetched:', data);
            this.employees = data;
          })
          .catch((error) => console.error('Error fetching employees:', error));
    },

    // ---- CLOCK IN/OUT ----
    clockIn() {
      if (!this.selectedEmployeeClock) return;
      fetch(`${baseURL}/clock_in/?employee_id=${this.selectedEmployeeClock}`, {
        method: 'POST',
      })
          .then((res) => res.json())
          .then((data) => {
            alert(data.message || data.detail);
          });
    },
    clockOut() {
      if (!this.selectedEmployeeClock) return;
      fetch(`${baseURL}/clock_out/?employee_id=${this.selectedEmployeeClock}`, {
        method: 'POST',
      })
          .then((res) => res.json())
          .then((data) => {
            alert(data.message || data.detail);
          })
          .catch((error) => {
            console.error('Error:', error);
            alert('An error occurred while clocking out.');
          });
    },
    startLunch() {
      if (!this.selectedEmployeeClock) return;
      fetch(`${baseURL}/start_lunch/?employee_id=${this.selectedEmployeeClock}`, {
        method: 'POST',
      })
          .then((res) => res.json())
          .then((data) => {
            alert(data.message || data.detail);
          })
          .catch((error) => {
            console.error('Error:', error);
            alert('An error occurred while starting lunch.');
          });
    },
    endLunch() {
      if (!this.selectedEmployeeClock) return;
      fetch(`${baseURL}/end_lunch/?employee_id=${this.selectedEmployeeClock}`, {
        method: 'POST',
      })
          .then((res) => res.json())
          .then((data) => {
            alert(data.message || data.detail);
          })
          .catch((error) => {
            console.error('Error:', error);
            alert('An error occurred while ending lunch.');
          });
    },

    // ---- LOGS ----
    viewLogs() {
      const nameFilter = this.logsFilter.name;
      const dateFrom = this.logsFilter.dateFrom;
      const dateTo = this.logsFilter.dateTo;

      let url = `${baseURL}/logs/?`;
      const params = [];
      if (nameFilter) {
        params.push(`employee_name=${encodeURIComponent(nameFilter)}`);
      }
      if (dateFrom) {
        params.push(`date_from=${dateFrom}`);
      }
      if (dateTo) {
        params.push(`date_to=${dateTo}`);
      }
      url += params.join('&');

      fetch(url)
          .then((res) => res.json())
          .then((data) => {
            this.logs = data;
          })
          .catch((error) => {
            console.error('Error:', error);
            alert('An error occurred while fetching logs.');
          });
    },

    // ---- SHIFTS ----
    createShift() {
      const {employee_id, date, start_time, end_time} = this.shiftFormData;
      if (!employee_id || !date || !start_time || !end_time) {
        alert('Please fill in all fields.');
        return;
      }

      fetch(`${baseURL}/shifts/`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
          employee_id: parseInt(employee_id),
          date,
          start_time,
          end_time,
        }),
      })
          .then((res) => {
            if (!res.ok) {
              return res.json().then((data) => {
                throw new Error(data.detail || 'Error creating shift.');
              });
            }
            return res.json();
          })
          .then(() => {
            alert('Shift created successfully.');
            this.shiftFormData.employee_id = null;
            this.shiftFormData.date = '';
            this.shiftFormData.start_time = '';
            this.shiftFormData.end_time = '';
            this.loadShifts();
          })
          .catch((error) => {
            console.error('Error:', error);
            alert(error.message);
          });
    },
    loadShifts() {
      const {employee_id, date_from, date_to} = this.shiftFilter;
      let url = `${baseURL}/shifts/?`;
      const params = [];

      if (employee_id) {
        params.push(`employee_id=${employee_id}`);
      }
      if (date_from) {
        params.push(`date_from=${date_from}`);
      }
      if (date_to) {
        params.push(`date_to=${date_to}`);
      }
      url += params.join('&');

      fetch(url)
          .then(async (res) => {
            if (!res.ok) {
              let err = 'Error fetching shifts.';
              try {
                const data = await res.json();
                err = data.detail || err;
              } catch {
              }
              throw new Error(err);
            }
            return res.json();
          })
          .then((data) => {
            this.shifts = Array.isArray(data) ? data : [];
          })
          .catch((error) => {
            console.error('Error:', error);
            alert(error.message);
          });
    },

    // ---- REPORTS ----
    generateAttendanceReport() {
      const {employee_id, date_from, date_to} = this.reportFilter;
      if (!employee_id || !date_from || !date_to) {
        alert('Please fill in all fields.');
        return;
      }

      const url = `${baseURL}/reports/attendance/?employee_id=${employee_id}&date_from=${date_from}&date_to=${date_to}`;
      fetch(url)
          .then((res) => res.json())
          .then((data) => {
            this.reportResult = data;
          })
          .catch((error) => {
            console.error('Error:', error);
            alert('An error occurred while generating the report.');
          });
    },

    // ---- LEAVE MANAGEMENT ----
    submitLeaveRequest() {
      const {employee_id, start_date, end_date, reason} = this.leaveRequest;
      if (!employee_id || !start_date || !end_date) {
        alert('Please fill in all required fields.');
        return;
      }

      fetch(`${baseURL}/leave_requests/`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
          employee_id: parseInt(employee_id),
          start_date,
          end_date,
          reason,
        }),
      })
          .then((res) => {
            if (!res.ok) {
              return res.json().then((data) => {
                throw new Error(data.detail || 'Error submitting leave request.');
              });
            }
            return res.json();
          })
          .then(() => {
            alert('Leave request submitted successfully.');
            this.leaveRequest.employee_id = null;
            this.leaveRequest.start_date = '';
            this.leaveRequest.end_date = '';
            this.leaveRequest.reason = '';
            this.loadLeaveRequests();
          })
          .catch((error) => {
            console.error('Error:', error);
            alert(error.message);
          });
    },
    loadLeaveRequests() {
      fetch(`${baseURL}/leave_requests/`)
          .then(async (res) => {
            if (!res.ok) {
              let err = 'Error fetching leave requests.';
              try {
                const data = await res.json();
                err = data.detail || err;
              } catch {
              }
              throw new Error(err);
            }
            return res.json();
          })
          .then((data) => {
            this.leaveRequests = Array.isArray(data) ? data : [];
          })
          .catch((error) => {
            console.error('Error:', error);
            alert(error.message);
          });
    },
    updateLeaveRequestStatus(leaveId, status) {
      fetch(`${baseURL}/leave_requests/${leaveId}/?status=${status}`, {
        method: 'PUT',
      })
          .then((res) => {
            if (!res.ok) {
              return res.json().then((data) => {
                throw new Error(data.detail || 'Error updating leave request.');
              });
            }
            return res.json();
          })
          .then(() => {
            alert(`Leave request ${status.toLowerCase()} successfully.`);
            this.loadLeaveRequests();
          })
          .catch((error) => {
            console.error('Error:', error);
            alert(error.message);
          });
    },

    // ---- EMPLOYEE MANAGEMENT ----
    createEmployee() {
      if (!this.employeeFormData.name) {
        alert('Please enter a name.');
        return;
      }
      fetch(`${baseURL}/employees/`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({name: this.employeeFormData.name}),
      })
          .then((res) => {
            if (!res.ok) {
              return res.json().then((data) => {
                throw new Error(data.detail || 'Error creating employee.');
              });
            }
            return res.json();
          })
          .then((newEmployee) => {
            alert('Employee created successfully.');
            this.employeeFormData.name = '';
            this.loadEmployees();
          })
          .catch((error) => {
            console.error(error);
            alert(error.message);
          });
    },
    deleteEmployee(employeeId) {
      if (!confirm('Are you sure you want to delete this employee?')) return;

      fetch(`${baseURL}/employees/${employeeId}/`, {
        method: 'DELETE',
      })
          .then(async (res) => {
            if (!res.ok) {
              let err = 'Error deleting employee.';
              try {
                const data = await res.json();
                err = data.detail || err;
              } catch {
              }
              throw new Error(err);
            }
            return res.json();
          })
          .then((data) => {
            alert(data.message || 'Employee deleted successfully.');
            this.loadEmployees();
          })
          .catch((error) => {
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
        alert('Invalid data.');
        return;
      }
      fetch(`${baseURL}/employees/${employee_id}/`, {
        method: 'PUT',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({name}),
      })
          .then((res) => {
            if (!res.ok) {
              return res.json().then((data) => {
                throw new Error(data.detail || 'Error updating employee.');
              });
            }
            return res.json();
          })
          .then((updatedEmployee) => {
            alert('Employee updated successfully.');
            this.cancelEdit();
            this.loadEmployees();
          })
          .catch((error) => {
            console.error(error);
            alert(error.message);
          });
    },
    cancelEdit() {
      this.editMode = false;
      this.employeeFormData.employee_id = null;
      this.employeeFormData.name = '';
    },
  },
};
</script>

<style scoped>
@import url('https://cdn.jsdelivr.net/npm/vuetify@3.3.7/dist/vuetify.min.css');
@import url('https://fonts.googleapis.com/css?family=Roboto:100,300,400,500,700,900');
@import url('https://cdn.jsdelivr.net/npm/@mdi/font@6.9.96/css/materialdesignicons.min.css');

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
