$(document).ready(function() {
   var substrate_humidity_set_point = 70.0;
   var solution_ph = 0.0;

   var system_status = {
      // Initial system status
      substrate_humidity_set_point: substrate_humidity_set_point,
      solution_ph_set_point: 0.0,
      env_temp: '-',
      env_humidity: '-',
      solution_temp: '-',
      solution_ph: solution_ph,
      solution_ph_data: [],
      substrate_humidity: '-',
      substrate_humidity_data: [],
      substrate_humidity_pump: 0,
      ph_up_pump: 0,
      ph_down_pump: 0,
      operation_mode: 'auto'
   };

   var chart_table = new CanvasJS.Chart("chart_table", {
      zoomEnabled: true,
      axisX: {
         gridThickness: 1,
         valueFormatString: "HH:mm:ss",
      },
      axisY: {
         title: "Umidade (%)",
         gridThickness: 1,
         stripLines: [{
            value: system_status.substrate_humidity_set_point,
            color:"#FF0000"
         }],
         minimum: 0,
         maximum: 100
      },
      // axisY2: {
      //    title: "pH",
      //    gridThickness: 1,
      //    stripLines: [{
      //       value: system_status.solution_ph_set_point,
      //       color:"#00FF00"
      //    }],
      //    minimum: 0,
      //    maximum: 14
      // },
      legend: {
         dockInsidePlotArea: true,
         horizontalAlign: "right",
         verticalAlign: "bottom",
         fontSize: 12
      },
      data: [
         {
            showInLegend: true,
            legendText: "Umidade do Substrato (%)",
            type: "spline",
            xValueType: "dateTime",
            dataPoints: system_status.substrate_humidity_data
         },
         // {
         //    showInLegend: true,
         //    legendText: "pH",
         //    type: "spline",
         //    axisYType: "secondary",
         //    xValueType: "dateTime",
         //    dataPoints: system_status.solution_ph_data,
         // }
      ]
   });

   var update_chart = function(chart, x_val, system_status) {
      var dataLength = 10 // number of dataPoints visible at any point
      system_status.substrate_humidity_data.push({
         x: x_val,
         y: system_status.substrate_humidity
      });
      if(system_status.substrate_humidity_data.length > dataLength) {
         system_status.substrate_humidity_data.shift();
      }

      // system_status.solution_ph_data.push({
      //    x: x_val,
      //    y: system_status.solution_ph
      // });
      // if(system_status.solution_ph_data.length > dataLength) {
      //    system_status.solution_ph_data.shift();
      // }

      chart.render();
   };

   update_chart(chart_table, new Date(), system_status);

   function _update_operation_buttons(operation_mode, system_status) {
      if(operation_mode === 'auto') {
         $('#action_solution_pump').prop("disabled", true);
      } else {
         $('#action_solution_pump').prop("disabled", false);
         if(system_status.substrate_humidity_pump === 1) {
            $('#action_solution_pump').val('Desligar Bomba Umidade Solucao');
         } else {
            $('#action_solution_pump').val('Ligar Bomba Umidade Solucao');
         }
      }
   };

   var wsuri;
   if(document.location.origin === "file://") {
      wsuri = "ws://127.0.0.1:8080/ws";
   } else {
      wsuri = (document.location.protocol === "http:" ? "ws:" : "wss:") + "//" +
               document.location.host + "/ws";
   }

   var connection = new autobahn.Connection({
      url: wsuri,
      realm: "realm1"
   });

   // fired when connection is established and session attached
   connection.onopen = function (session, details) {
      // Action buttons
      $("#action_solution_humidity_set_point").click(function() {
         substrate_humidity_set_point = $("#substrate_humidity_set_point").val();
         system_status.substrate_humidity_set_point = parseFloat(substrate_humidity_set_point);
         chart_table.options.axisY.stripLines[0].value = system_status.substrate_humidity_set_point;
         chart_table.render();
         session.publish('com.ebbandflow.onwrite', [
            {substrate_humidity_set_point: substrate_humidity_set_point}]);
      });
      // $("#action_solution_ph_set_point").click(function() {
      //    var solution_ph_set_point = $("#solution_ph_set_point").val();
      //    system_status.solution_ph_set_point = parseFloat(solution_ph_set_point);
      //    chart_table.options.axisY2.stripLines[0].value = system_status.solution_ph_set_point;
      //    chart_table.render();
      //    session.publish('com.ebbandflow.onwrite', [{
      //       'solution_ph_set_point': solution_ph_set_point
      //    }]);
      // });
      $('#action_solution_pump').click(function() {
         var actual_status = system_status.substrate_humidity_pump;
         if(actual_status === 0) {
            new_status = 1;
            $('#action_solution_pump').val('Desligar Bomba Umidade Solucao');
            $("#substrate_humidity_pump").html("ON");
            $("#substrate_humidity_pump_line").toggleClass("success", true);
         } else {
            new_status = 0;
            $('#action_solution_pump').val('Ligar Bomba Umidade Solucao');
            $("#substrate_humidity_pump").html("OFF");
            $("#substrate_humidity_pump_line").toggleClass("success", false);
         }
         system_status.substrate_humidity_pump = new_status;
         session.publish('com.ebbandflow.onwrite', [{
            'substrate_humidity_pump': new_status
         }]);
      });
      // $('#action_ph_up_pump').click(function() {
      //    alert('Mudar status bomba de pH up');
      // });
      // $('#action_ph_down_pump').click(function() {
      //    alert('Mudar status bomba de ph down');
      // });
      // $('#action_ph_read').click(function() {
      //    alert('Ler pH');
      // });
      $('input[name="operation_mode"]').click(function() {
         var next_status = $('input[name=operation_mode]:checked').val();
         system_status.operation_mode = next_status;
         session.publish('com.ebbandflow.onwrite', [{
            'operation_mode': next_status
         }]);

         // console.log(nex)

         session.call('com.ebbandflow.comando_serial', ['m0']).then(
            function (res) {
               session.call('com.ebbandflow.comando_serial', ['b1'])
            },
            function (err) {
               console.log("add2() error:", err);
            }
         );

         _update_operation_buttons(next_status, system_status);
      });

      function on_read(args) {
         // Executed when data is received from the plant
         var data = args[0];
         console.log("Data received: " + data);

         // Actuators status
         if('substrate_humidity_pump' in data) {
            if(data.substrate_humidity_pump === 1) {
               $("#substrate_humidity_pump").html("ON");
               $("#substrate_humidity_pump_line").toggleClass("success", true);
            } else {
               $("#substrate_humidity_pump").html("OFF");
               $("#substrate_humidity_pump_line").toggleClass("success", false);
            }
         }

         if('substrate_humidity_set_point' in data) {
            $("#substrate_humidity_set_point").val(data.substrate_humidity_set_point);
            system_status.substrate_humidity_set_point = parseFloat(substrate_humidity_set_point);
            chart_table.options.axisY.stripLines[0].value = system_status.substrate_humidity_set_point;
            chart_table.render();            
         }

         if('operation_mode' in data) {
            if(data.operation_mode === 'auto') {
               $('input:radio[name=operation_mode][value=auto]').prop('checked', true);
            } else {
               $('input:radio[name=operation_mode][value=manual]').prop('checked', true);
            }
            _update_operation_buttons(data.operation_mode, system_status);
         }



         // // Sensor values
         values_to_read = [
            'env_temp', 'env_humidity', 'solution_temp',
            'solution_ph', 'substrate_humidity'
         ]
         for(var i = 0; i < values_to_read.length; i++) {
            value_key = values_to_read[i];
            if(value_key in data) {
               system_status[value_key] = data[value_key];
               $('#' + value_key).html(data[value_key]);
            }
         }

         // // Update chart
         if('substrate_humidity' in data) {
            update_chart(chart_table, new Date(), system_status);
         }
      }

      session.subscribe('com.ebbandflow.onread', on_read).then(
         function (sub) {
            console.log('subscribed to topic');
         },
         function (err) {
            console.log('failed to subscribe to topic', err);
         }
      );
   };

   // fired when connection was lost (or could not be established)
   connection.onclose = function (reason, details) {
      console.log("Connection lost: " + reason);
   }

   // now actually open the connection
   connection.open();
});