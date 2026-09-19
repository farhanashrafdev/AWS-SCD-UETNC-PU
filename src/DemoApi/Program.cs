using DemoApi.Services;
using Microsoft.AspNetCore.Authentication;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();
builder.Services.AddSingleton<UserService>();

// Demo-only authentication: the caller sends "X-Demo-User: <id>".
// A real system would use OpenID Connect / JWT bearer tokens instead.
builder.Services
    .AddAuthentication(DemoAuthenticationHandler.SchemeName)
    .AddScheme<AuthenticationSchemeOptions, DemoAuthenticationHandler>(
        DemoAuthenticationHandler.SchemeName, options => { });

builder.Services.AddAuthorization();

var app = builder.Build();

app.UseAuthentication();
app.UseAuthorization();
app.MapControllers();

// Used by the Kubernetes readiness/liveness probes in
// gitops/manifests/demo-api/deployment.yaml.
app.MapGet("/health", () => Results.Ok(new { status = "healthy" }))
    .AllowAnonymous();

app.Run();

// Lets the test project reference the app through WebApplicationFactory<Program>.
public partial class Program { }
