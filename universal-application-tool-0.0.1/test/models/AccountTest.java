package models;

import static org.assertj.core.api.Assertions.assertThat;

import org.junit.Before;
import org.junit.Test;
import repository.UserRepository;
import repository.WithPostgresContainer;
import services.program.ProgramDefinition;
import support.ProgramBuilder;

public class AccountTest extends WithPostgresContainer {

  private UserRepository repository;

  @Before
  public void setup() {
    repository = instanceOf(UserRepository.class);
  }

  @Test
  public void canAddAdministeredProgram() {
    Account account = new Account();
    String email = "fake email";
    account.setEmailAddress(email);

    ProgramDefinition one = ProgramBuilder.newDraftProgram("one").build().getProgramDefinition();
    ProgramDefinition two = ProgramBuilder.newDraftProgram("two").build().getProgramDefinition();
    account.addAdministeredProgram(one);
    account.addAdministeredProgram(two);

    account.save();

    Account found = repository.lookupAccount(email).get();
    assertThat(found.getAdministeredProgramNames()).containsExactly("one", "two");
  }

  @Test
  public void addDuplicateProgram_doesNotAddToList() {
    Account account = new Account();
    String programName = "duplicate";
    ProgramDefinition program = ProgramBuilder.newDraftProgram(programName).buildDefinition();

    account.addAdministeredProgram(program);
    assertThat(account.getAdministeredProgramNames()).containsOnly(programName);

    // Try to add again.
    account.addAdministeredProgram(program);
    assertThat(account.getAdministeredProgramNames()).containsExactly(programName);
  }
}