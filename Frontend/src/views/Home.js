// reactstrap components
import {
  Card, CardBody, CardHeader, CardImg, CardText, CardTitle, Col, Row
} from "reactstrap";
import homeimg from '../assets/img/Home1.jpg';

function Home(props) {
  return (
    <>
      <div className="content">
        <Row>
          <Col lg="12">
            <Card>
              <CardHeader>
                <CardTitle tag="h1">WELCOME TO SCOUT APP</CardTitle>
              </CardHeader>
              <CardBody>
                <Row>
                  <Col lg="4" md="6">
                    <CardImg top width="100%" src={homeimg} alt="Card image cap" />
                  </Col>
                  <Col lg="8" md="6">
                    <CardText tag="h4">The Indian Premier League (IPL) is a professional Twenty20 cricket league contested by eight teams based on eight different Indian cities. The league was founded by the Board of Control for Cricket in India (BCCI) in 2007. It is usually held between March and May of every year and has an exclusive window in the ICC Future Tours Programme.</CardText>
                    <br></br>
                    <CardText tag="h4">The IPL is the most-attended cricket league globally and in 2014 was ranked sixth by average attendance among all sports leagues. In 2010, the IPL became the first sporting event to be broadcast live on YouTube. The brand value of the IPL in 2019 was ₹475 billion (US$6.7 billion), according to Duff & Phelps. According to BCCI, the 2015 IPL season contributed ₹11.5 billion (US$160 million) to the GDP of the Indian economy.</CardText>
                    <br></br>
                    <CardText tag="h4">This Application aims to find the best suitable cricket players to target during the auction by predicting their upcoming performance based on the current statistics.</CardText>
                    <br></br>
                  </Col>
                </Row>
              </CardBody>
            </Card>
          </Col>
        </Row>
      </div>
    </>
  );
}

export default Home;
