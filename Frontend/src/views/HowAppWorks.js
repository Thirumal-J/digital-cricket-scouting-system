// reactstrap components
import {
  Card, CardBody, CardHeader, CardTitle, Col, Row
} from "reactstrap";

function HowAppWorks(props) {

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
