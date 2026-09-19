using System.Security.Claims;
using DemoApi.Models;
using DemoApi.Services;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace DemoApi.Controllers;

[ApiController]
[Route("api/users")]
public class UsersController(UserService users) : ControllerBase
{
    /// <summary>
    /// GET /api/users/{id}
    /// Returns a user's profile. Two checks protect it:
    ///   1. Authentication: [Authorize] rejects anonymous callers (401).
    ///   2. Authorization: the caller may only read their own record (403).
    /// </summary>
    [HttpGet("{id:int}")]
    [Authorize]
    public ActionResult<UserDto> GetUser(int id)
    {
        var callerId = User.FindFirstValue(ClaimTypes.NameIdentifier);

        // Resource-level check: being logged in is not enough.
        // Without this, any authenticated user could read any other user's data.
        if (callerId != id.ToString())
        {
            return Forbid();
        }

        var user = users.GetById(id);
        return user is null ? NotFound() : Ok(user);
    }
}
