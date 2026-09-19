using System.Net;
using System.Net.Http.Json;
using DemoApi.Models;
using Microsoft.AspNetCore.Mvc.Testing;
using Xunit;

namespace DemoApi.Tests;

/// <summary>Authorization regression tests that a missing-authorization demo PR is expected to break.</summary>
public class AuthorizationTests(WebApplicationFactory<Program> factory) : IClassFixture<WebApplicationFactory<Program>>
{
    private const string DemoUserHeader = "X-Demo-User";

    [Fact]
    public async Task GetUser_WithoutAuthentication_ReturnsUnauthorized()
    {
        using var client = factory.CreateClient();

        var response = await client.GetAsync("/api/users/1");

        // This is intentionally the key regression test for the demo: removing [Authorize] changes this from 401 to 200.
        Assert.Equal(HttpStatusCode.Unauthorized, response.StatusCode);
    }

    [Fact]
    public async Task GetUser_RequestingOwnRecord_ReturnsOk()
    {
        using var client = factory.CreateClient();
        client.DefaultRequestHeaders.Add(DemoUserHeader, "1");

        var response = await client.GetAsync("/api/users/1");
        var user = await response.Content.ReadFromJsonAsync<UserDto>();

        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
        Assert.NotNull(user);
        Assert.Equal("Alice", user.DisplayName);
    }

    [Fact]
    public async Task GetUser_RequestingAnotherUsersRecord_ReturnsForbidden()
    {
        using var client = factory.CreateClient();
        client.DefaultRequestHeaders.Add(DemoUserHeader, "1");

        var response = await client.GetAsync("/api/users/2");

        // This also fails if the ownership check is removed, which is part of the same demo vulnerability as the anonymous access case.
        Assert.Equal(HttpStatusCode.Forbidden, response.StatusCode);
    }

    [Fact]
    public async Task GetUser_RequestingUnknownId_ReturnsNotFound()
    {
        using var client = factory.CreateClient();
        client.DefaultRequestHeaders.Add(DemoUserHeader, "999");

        var response = await client.GetAsync("/api/users/999");

        Assert.Equal(HttpStatusCode.NotFound, response.StatusCode);
    }
}
