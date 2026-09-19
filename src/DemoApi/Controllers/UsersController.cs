using DemoApi.Models;
using DemoApi.Services;
using Microsoft.AspNetCore.Mvc;

namespace DemoApi.Controllers;

[ApiController]
[Route("api/users")]
public class UsersController(UserService users) : ControllerBase
{
    /// <summary>
    /// GET /api/users/{id}
    /// Returns a user's profile.
    /// </summary>
    [HttpGet("{id:int}")]
    public ActionResult<UserDto> GetUser(int id)
    {
        var user = users.GetById(id);
        return user is null ? NotFound() : Ok(user);
    }
}
