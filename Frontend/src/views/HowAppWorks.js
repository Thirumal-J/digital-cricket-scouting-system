import React from "react";
// reactstrap components
import {
  Card,
  CardHeader,
  CardBody,
  CardTitle,
  Row,
  Col,
} from "reactstrap";

function HowAppWorks(props) {
  // const [bigChartData, setbigChartData] = React.useState("data1");
  // const setBgChartData = (name) => {
  //   setbigChartData(name);
  // };
  return (
    <>
      <div className="content">
        <Row>
        <Col lg="6" md="12">
            <Card>
              <CardHeader>
                <CardTitle tag="h2">Take a tour and find out how the application is working!!</CardTitle>
              </CardHeader>
              <CardBody>
                
              </CardBody>
            </Card>
          </Col>
        </Row>
      </div>
    </>
  );
}

export default HowAppWorks;
