package com.example.lab5;

import androidx.appcompat.app.AppCompatActivity;

import android.graphics.Color;
import android.os.Bundle;
import android.os.CountDownTimer;
import android.util.Log;
import android.view.View;
import android.widget.TextView;

import com.github.angads25.toggle.interfaces.OnToggledListener;
import com.github.angads25.toggle.model.ToggleableView;
import com.github.angads25.toggle.widget.LabeledSwitch;

import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallbackExtended;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;

import java.nio.charset.Charset;
import java.util.Timer;
import java.util.TimerTask;


public class MainActivity extends AppCompatActivity {
    MQTTHelper mqttHelper;
    TextView  txtHumi,txtPump,txtVision,txtConnect,txtTime;
    LabeledSwitch btnLED, btnPUMP;
    public int count = 0;
    CountDownTimer flag = new CountDownTimer(0, 1000){
        public void onTick(long millisUntilFinished){

        }
        public  void onFinish(){
        }
    }.start();
    @Override

    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        txtConnect = findViewById(R.id.txtConnection);
        txtHumi = findViewById(R.id.txtHumidity);
        txtPump = findViewById(R.id.txtPump);
        txtVision = findViewById(R.id.txtVision);
        btnLED =  findViewById(R.id.btnLED);
        btnPUMP = findViewById(R.id.btnPUMP);
        txtTime = findViewById(R.id.txtTime);
        btnLED.setOnToggledListener(new OnToggledListener() {
            @Override
            public void onSwitched(ToggleableView toggleableView, boolean isOn) {
                if(isOn == true){
                    sendDataMQTT("xuan_bach/feeds/nutnhan1","1");
                }else if (isOn==false){
                    sendDataMQTT("xuan_bach/feeds/nutnhan1","0");
                }
//                count = 7;
//                flag = new CountDownTimer(7000, 1000){
//                    public void onTick(long millisUntilFinished){
//                        txtTime.setText("try to reconnect in "+ count + "s");
//                        count--;
//                    }
//                    public  void onFinish(){
//                        btnLED.setEnabled(false);
//                        btnPUMP.setEnabled(false);
//                        txtConnect.setText("connection failed");
//
//                    }
//                }.start();

            }

        });
        btnPUMP.setOnToggledListener(new OnToggledListener() {
            @Override
            public void onSwitched(ToggleableView toggleableView2, boolean isOn2) {
                if(isOn2 == true){
                    sendDataMQTT("xuan_bach/feeds/nutnhan2","2");
                }else if (isOn2==false){
                    sendDataMQTT("xuan_bach/feeds/nutnhan2","3");
                }

            }
        });

        startMQTT();

    }
    public void sendDataMQTT(String topic, String value){
        MqttMessage msg = new MqttMessage();
        msg.setId(1234);
        msg.setQos(0);
        msg.setRetained(false);

        byte[] b = value.getBytes(Charset.forName("UTF-8"));
        msg.setPayload(b);
        try {
            mqttHelper.mqttAndroidClient.publish(topic, msg);
        }catch (MqttException e){
        }
    }

    public void startMQTT(){
        mqttHelper = new MQTTHelper(this);
        mqttHelper.setCallback(new MqttCallbackExtended() {

            @Override
            public void connectComplete(boolean reconnect, String serverURI) {
//                btnPUMP.setVisibility(View.VISIBLE);
//                count = 0;
//                flag.cancel();
//                btnLED.setEnabled(true);
//                btnPUMP.setEnabled(true);
//                txtConnect.setText("connected");
                txtConnect.setText("connection failed");
                btnLED.setEnabled(false);
                btnPUMP.setEnabled(false);

            }

            @Override
            public void connectionLost(Throwable cause) {
//                count = 0;
//                flag = new CountDownTimer(10000, 1000){
//                    public void onTick(long millisUntilFinished){
//                        txtConnect.setText("try to reconnect in "+ count + "s");
//                        count++;
//                    }
//                    public  void onFinish(){
//                        btnLED.setEnabled(false);
//                        btnPUMP.setEnabled(false);
//                        txtConnect.setText("connection failed");
//
//                    }
//                }.start();

            }

            @Override
            public void messageArrived(String topic, MqttMessage message) throws Exception {

                Log.d("TEST", topic + "***" + message.toString());
                if (topic.contains("xuan_bach/feeds/pump")) {
                    sendDataMQTT("xuan_bach/feeds/ok","2");
                    txtPump.setText(message.toString() + "L");
                } else if (topic.contains("xuan_bach/feeds/aivision")) {
                    btnLED.setColorBorder(Color.parseColor("@color/colorAccent"));
                    btnPUMP.setColorBorder(Color.parseColor("ffff00"));
                    txtVision.setText(message.toString() + "<3");
                } else if (topic.contains("xuan_bach/feeds/humid")) {
                    sendDataMQTT("xuan_bach/feeds/ok","1");
                    txtHumi.setText(message.toString() + "%");
                } else if (topic.contains("xuan_bach/feeds/ack")) {
                    if(message.toString().equals("1")) {
                        count = 7;
                        flag.cancel();
                        flag = new CountDownTimer(8000, 1000) {
                            public void onTick(long millisUntilFinished) {
//                            txtTime.setText("try to reconnect in "+ count + "s");
                                if (count % 2 == 0) {
                                    txtTime.setText("Waiting " + (7 - count) / 2 + " times");
                                } else {
                                    txtTime.setText("Sending " + (7 - count) / 2 + " times");
                                }
                                count--;
                            }

                            public void onFinish() {
//                            if(count == 0) {
                                btnLED.setEnabled(false);
                                btnPUMP.setEnabled(false);
                                btnLED.setColorBorder(Color.GRAY);
                                btnPUMP.setColorBorder(Color.GRAY);
                                txtConnect.setText("connection failed");
                                txtTime.setText("Block!!!");
//                            }

                            }
                        }.start();
                    }else if(message.toString().equals("0")){
                        flag.cancel();
                        txtConnect.setText("connect");
                        btnLED.setEnabled(true);
                        btnPUMP.setEnabled(true);
                        btnLED.setColorBorder(Color.parseColor("@color/colorAccent"));
                        btnPUMP.setColorBorder(Color.parseColor("ffff00"));
                        txtTime.setText("Streaming");
                    }
                } else if (topic.contains("xuan_bach/feeds/nutnhan2")) {
                    if (message.toString().equals("2")) {
                        btnPUMP.setOn(true);
                        btnPUMP.setOn(false);
                    }
                } else if (topic.contains("xuan_bach/feeds/nutnhan1")) {
                    if (message.toString().equals("1")) {
                        btnLED.setOn(true);
                        btnLED.setOn(false);
                    }
                }

            }

            @Override
            public void deliveryComplete(IMqttDeliveryToken token) {

            }
        });
    }
}