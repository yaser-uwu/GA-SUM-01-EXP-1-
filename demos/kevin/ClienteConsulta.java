import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;

public class ClienteConsulta {
    public static void main(String[] args) throws Exception {
        if (args.length != 1 || !args[0].matches("[1-9][0-9]{0,15}")) {
            System.err.println("Uso: java ClienteConsulta.java ID_DEL_TURNO");
            System.exit(2);
        }
        URI uri = URI.create("http://127.0.0.1:8082/api/consulta/turnos/" + args[0]);
        var builder = HttpRequest.newBuilder(uri).timeout(Duration.ofSeconds(8)).header("Accept", "application/json").GET();
        String token = System.getenv("RTV_TOKEN");
        if (token != null && !token.isBlank()) builder.header("Authorization", "Bearer " + token.trim());
        var client = HttpClient.newBuilder().connectTimeout(Duration.ofSeconds(5)).build();
        var response = client.send(builder.build(), HttpResponse.BodyHandlers.ofString());
        System.out.println("GET " + uri);
        System.out.println("HTTP " + response.statusCode());
        System.out.println("Content-Type: " + response.headers().firstValue("Content-Type").orElse(""));
        System.out.println(response.body());
        if (response.statusCode() != 200) System.exit(1);
    }
}
