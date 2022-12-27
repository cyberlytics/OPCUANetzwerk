import { Injectable } from '@angular/core';
import { LineChartDataSeries } from '../pages/SensorNode/lineChartComponent/LineChartDataClass';
import { AirQualityData } from '../pages/SensorNode/AirQuality/AirQualityChart/air-quality-data';
import { AirQualityTableData } from '../pages/SensorNode/AirQuality/air-quality-list-data';

@Injectable({
  providedIn: 'root'
})
export class DashboardFunctionalityService {

  constructor() { }

  /**
   * Checks if the Date is correct
   * 
   * @param {any}  date - Date that needs to be checked
   * @returns if Date is correct or not 
   * 
   */
  isCorrectDate(date) {
    if (date instanceof Date) {
      var text = Date.prototype.toString.call(date);
      return text !== 'Invalid Date';
    }
    return false;
  }

  /**
   * create an array from the result where the elements are structured like this [[timestamp, value]]
   * 
   * @param {any}  result - Received sensor data
   * @returns Structured Array  [[timestamp, value]]
   * 
   */
  mapResult(result: any) {
    let mapped = result.map(function (el) {
      return [el.timestamp, el.value];
    });
    return mapped;
  }


  /**
   * get the timestamp of each datapoint and convert it into a date object, the convert the date into an iso string
   * this is needed because the chart component does not support the date format from the backend
   * 
   * @param {any}  mapped - Mapped Data (Timestamp, Value)
   * @returns Converted data into an ISO string
   * 
   */
  convertMappedDate(mapped: any) {
    mapped.forEach(function (el) {
      let date = new Date(el[0]);
      el[0] = date.toISOString();
    });
    return mapped;
  }


  /**
   * We need new instances of LineChartDataSeries because only changing the properties of it does not trigger the change detection
   * this is because the reference to the object does not change
   * 
   * @param {string}  name - Name of Sensortype (AirPressure)
   * @param {any}  mapped - Mapped Data
   * @returns New instances of LineChartDataSeries
   * 
   */
  lineChartData(name: string, mapped: any) {
    let newData: LineChartDataSeries = {
      name: name,
      type: "line",
      data: mapped
    };
    return newData
  }

  /**
   * Saves the start and end timestamp for one value.
   * 
   * @param {any}  mappedPresence - MappedPresence data
   * @returns ganttData like this: [starttime, endtime, value]
   * 
   */
  gantArray(mappedPresence: any){
    let ganttArr = []
    let tempArr = []
    let present = false;
    let absent = false;

    for (let i = 0; i < mappedPresence.length; i++) {
      for (let j = 0; j < mappedPresence[i].length; j++) {
        if (mappedPresence[i][1] == 0) {
          tempArr.push(mappedPresence[i][0]);
          absent = true;
          if (absent == true && present == true) {
            present = false;
            absent = false;
            ganttArr.push([tempArr[0], tempArr[tempArr.length - 1], 1])
            tempArr = []
            tempArr.push(mappedPresence[i][0]);
          }
        }
        else if (mappedPresence[i][1] == 1) {
          tempArr.push(mappedPresence[i][0]);
          present = true;
          if (absent == true && present == true) {
            present = false;
            absent = false;
            ganttArr.push([tempArr[0], tempArr[tempArr.length - 1], 0])
            tempArr = []
            tempArr.push(mappedPresence[i][0]);
          }
        }
        else {
          console.log("No Value! What happened?");
        }
      }
    }
    return ganttArr
  }


  /**
   * New Gantt Instance for updating properties.
   * 
   * @param {any}  mapped - Mapped Data
   * @returns structured yAxis Data and xAxis Data in an Array
   * 
   */
  gantData(mapped: any) {
    let data = []
    for (var i = 0; i < mapped.length; i++) {
      for (let j = 0; j < 1; j++) {
        data.push({
          name: "Presence",
          value: [mapped[i][0], mapped[i][1], mapped[i][2]]
        });
      }
    }
    let newData = {
      "xAxis": data,
      "yAxis": ["Presence"],
    };
    return newData
  }

  /**
  * cleans the motian data
  * Motion data should always be 1 and 0 alternating
  * this function removes excess 1s and 0s
  * motion data is structured like this: [[timestamp, value]]
  * 
  * @param {any}  data - Motion Data: [[timestamp, value]]
  * @returns cleared motion data
  * 
  */
  cleanMotianData(data: any) {
    var cleanedData = [];
    var lastValue = null;
    for (var i = 0; i < data.length; i++) {
      if (data[i][1] != lastValue) {
        cleanedData.push(data[i]);
        lastValue = data[i][1];
      }
    }
    return cleanedData; 
  }


  /**
  * This function takes the mappedPresence array and generates a dataset for the gantt chart
  * the dataset should look like this [{name: "Presence", value: [start, end, 0/1]}]
  * the start and end values are the timestamps between which the value is 0 or 1
  * example: if "2022-12-22T12:39:21.251Z" is 1 and "2022-12-22T13:39:21.251Z" is 0, 
  * the dataset should look like this: [{name: "Presence", value: ["2022-12-22T12:39:21.251Z", "2022-12-22T13:39:21.251Z", 1]}]
  * example2: if "2022-12-22T12:39:21.251Z" is 0 and "2022-12-22T13:39:21.251Z" is 1, the dataset should look like this: [{name: "Presence", value: ["2022-12-22T12:39:21.251Z", "2022-12-22T13:39:21.251Z", 0]}]
  * 
  * @param {any}  data - mapped data: [[timestamp, value]]
  * @returns dataset like this: [{name: "Presence", value: [start, end, 0/1]}]
  * 
  */
  generateMotionDataset(data: any) {
    var ganttData = [];
    for (var i = 0; i < data.length; i++) {

      var ele = []
      if (i == 0) {
        //     START       END             VALUE
        ele = [data[i][0], data[i + 1][0], data[i][1]];
      }
      else if (i == data.length - 1) {
        //     START       END             VALUE
        ele = [data[i - 1][0], data[i][0], data[i][1]];
      }
      else {
        //     START       END             VALUE
        ele = [data[i - 1][0], data[i][0], data[i][1]];
      }

      ganttData.push({
        name: "Presence",
        value: ele
      });
    }
    return ganttData;
  }
  

  AirQuality: AirQualityData = {
    data: [],
  }
  AirQualityList: AirQualityTableData[] = [];

  /**
  * A function that calculates averages for the air quality for each day. 
  * It also calculates the delata to the day before.
  * It takes data in the form of the Interface AirQualityData and outputs an array in the form of the Interface AirQualityTableData
  * The final data represents average airquality levels for each day and the delta to the day before
  * 
  * @param {AirQualityData}  data - AirQuality Data
  * @returns Result
  * 
  */
  calculateAirQualityTableData(data: AirQualityData): AirQualityTableData[] {

    if (!data || !data.data || data.data.length == 0) {
      return [];
    }

    //sort the data by date the date is in string so we need to convert it to a date object before
    data.data.sort(function (a, b) {
      var dateA = new Date(a[0]);
      var dateB = new Date(b[0]);
      return dateA.getTime() - dateB.getTime();
    });

    //now we need to group the data by day
    var dayGroup = [];
    data.data.forEach(function (el) {
      var date = new Date(el[0]);
      var day = date.getDate();
      var month = date.getMonth() + 1;
      var year = date.getFullYear();

      var dayString = day + "." + month + "." + year;

      if (!dayGroup[dayString]) {
        dayGroup[dayString] = [];
      }
      dayGroup[dayString].push(el[1]);
    });

    //now we need to calculate the average for each day
    var result2 = [];
    for (var key in dayGroup) {
      var sum = 0;
      var count = 0;
      dayGroup[key].forEach(function (el) {
        sum += el;
        count++;
      });

      result2.push({
        day: key,
        average: sum / count
      });
    }

    //on the first element on the array we set the delta to 0
    result2[0].delta = 0;

    //now we need to calculate the delta to the day before
    for (var i = 1; i < result2.length; i++) {
      var delta = result2[i].average - result2[i - 1].average;
      result2[i].delta = delta;
      //if the delta is positive, we add set the down attribute to false, if it is negative we set it to true
      result2[i].down = delta < 0;
    }

    return result2;
  }

}

