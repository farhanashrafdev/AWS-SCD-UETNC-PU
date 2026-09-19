using System.Security.Claims;
using System.Text.Encodings.Web;
using DemoApi.Models;
using Microsoft.AspNetCore.Authentication;
using Microsoft.Extensions.Options;

namespace DemoApi.Services;

/// <summary>
/// In-memory "database" of users. Real systems would query a data store.
/// </summary>
public class UserService
{
    private static readonly Dictionary<int, UserDto> Users = new()
    {
        [1] = new UserDto(1, "Alice", "alice@example.com"),
        [2] = new UserDto(2, "Bob", "bob@example.com"),
    };

    public UserDto? GetById(int id) => Users.TryGetValue(id, out var user) ? user : null;
}

/// <summary>
/// Demo-only authentication. The request header "X-Demo-User: 1" means
/// "I am user 1". This is obviously not secure and exists only so the
/// authorization logic can be shown and tested without an identity provider.
/// </summary>
public class DemoAuthenticationHandler(
    IOptionsMonitor<AuthenticationSchemeOptions> options,
    ILoggerFactory logger,
    UrlEncoder encoder)
    : AuthenticationHandler<AuthenticationSchemeOptions>(options, logger, encoder)
{
    public const string SchemeName = "Demo";
    public const string HeaderName = "X-Demo-User";

    protected override Task<AuthenticateResult> HandleAuthenticateAsync()
    {
        if (!Request.Headers.TryGetValue(HeaderName, out var value) ||
            !int.TryParse(value, out var userId))
        {
            return Task.FromResult(AuthenticateResult.NoResult());
        }

        var identity = new ClaimsIdentity(
            [new Claim(ClaimTypes.NameIdentifier, userId.ToString())],
            SchemeName);

        var ticket = new AuthenticationTicket(new ClaimsPrincipal(identity), SchemeName);
        return Task.FromResult(AuthenticateResult.Success(ticket));
    }
}
