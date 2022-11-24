package com.example.lab5;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.util.Log;
import android.widget.TextView;

import com.github.angads25.toggle.interfaces.OnToggledListener;
import com.github.angads25.toggle.model.ToggleableView;
import com.github.angads25.toggle.widget.LabeledSwitch;

import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallbackExtended;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;

import java.nio.charset.Charset;

public class MainActivity extends AppCompatActivity {
    MQTTHelper mqttHelper;
    TextView txtTemp, txtHumi,txtLed,txtPump,txtVision;
    LabeledSwitch btnLED, btnPUMP;
    @Override

    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        txtTemp = findViewById(R.id.txtTemperature);
        txtHumi = findViewById(R.id.txtHumidity);
        txtLed = findViewById(R.id.txtLed);
        txtPump = findViewById(R.id.txtPump);
        txtVision = findViewById(R.id.txtVision);
        btnLED =  findViewById(R.id.btnLED);
        btnPUMP = findViewById(R.id.btnPUMP);

        btnLED.setOnToggledListener(new OnToggledListener() {
            @Override
            public void onSwitched(ToggleableView toggleableView, boolean isOn) {
                if(isOn == true){
                    sendDataMQTT("xuan_bach/feeds/nutnhan1","1");
                }else{
                    sendDataMQTT("xuan_bach/feeds/nutnhan1","0");
                }
            }
        });
        btnPUMP.setOnToggledListener(new OnToggledListener() {
            @Override
            public void onSwitched(ToggleableView toggleableView2, boolean isOn2) {
                if(isOn2 == true){
                    sendDataMQTT("xuan_bach/feeds/nutnhan2","2");
                }else{
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

            }

            @Override
            public void connectionLost(Throwable cause) {

            }

            @Override
            public void messageArrived(String topic, MqttMessage message) throws Exception {
                Log.d("TEST",topic + "***" + message.toString());
                if(topic.contains("xuan_bach/feeds/pump")){
                    txtPump.setText(message.toString()+"L");
                }else if(topic.contains("xuan_bach/feeds/aivision")){
                    txtVision.setText(message.toString() + "<3");
                }else if(topic.contains("xuan_bach/feeds/led")){
                    txtLed.setText(message.toString() + "%");
                }else if(topic.contains("xuan_bach/feeds/humid")){
                    txtHumi.setText(message.toString() + "%");
                }else if(topic.contains("xuan_bach/feeds/temp")){
                    txtTemp.setText(message.toString() + "°C");
                }else if (topic.contains("nutnhan1")){
                    if(message.toString().equals("1") ){
                        btnPUMP.setOn(true);
                    }else{
                        btnPUMP.setOn(false);
                    }
                }else if (topic.contains("nutnhan2")){
                    if(message.toString().equals("2") ){
                        btnLED.setOn(true);
                    }else{
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