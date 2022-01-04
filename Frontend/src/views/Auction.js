import React from "react";
import {
  Card,
  CardHeader,
  CardBody,
  CardTitle,
  Row,
  Col,
} from "reactstrap";

function Auction(props) {

  const [chartData, setChartData] = useState({
      rating5Count: 0,
      rating4Count: 0,
      rating3Count: 0,
      rating2Count: 0,
      rating1Count: 0,
      role:""
  });

  let chart = {
    data: (canvas) => {
      let ctx = canvas.getContext("2d");

      let gradientStroke = ctx.createLinearGradient(0, 230, 0, 50);

      gradientStroke.addColorStop(1, "rgba(29,140,248,0.2)");
      gradientStroke.addColorStop(0.4, "rgba(29,140,248,0.0)");
      gradientStroke.addColorStop(0, "rgba(29,140,248,0)"); //blue colors

      return {
        labels: ["Excellent Performer", "Good Performer", "Above Average Performer", "Average Performer", "Poor Performer"],
        datasets: [
          {
            label: "Data",
            fill: true,
            backgroundColor: gradientStroke,
            borderColor: "#1f8ef1",
            borderWidth: 2,
            borderDash: [],
            borderDashOffset: 0.0,
            pointBackgroundColor: "#1f8ef1",
            pointBorderColor: "rgba(255,255,255,0)",
            pointHoverBackgroundColor: "#1f8ef1",
            pointBorderWidth: 20,
            pointHoverRadius: 4,
            pointHoverBorderWidth: 15,
            pointRadius: 4,
            data: [chartData.rating5Count, chartData.rating5Count, chartData.rating5Count, chartData.rating5Count, chartData.rating5Count],
          },
        ],
      };
    },
    options: chart1_2_options,
  };

  return (
    <>
      <div className="content">
        <Row>
          <Col lg="6" md="12">
            <Card>
              <CardHeader>
                <CardTitle tag="h2">The ultimate guide for better auction strategy</CardTitle>
              </CardHeader>
              <CardBody>

                <div className="chart-area">
                  <Bar
                    data={chart.data}
                    options={chart.options}
                  />
                </div>
                <div className="chart-area">
                  <Bar
                    data={chart.data}
                    options={chart.options}
                  />
                </div>
                <div className="chart-area">
                  <Bar
                    data={chart.data}
                    options={chart.options}
                  />
                </div>
              </CardBody>
            </Card>
          </Col>
        </Row>
      </div>
    </>
  );
}

export default Auction;
